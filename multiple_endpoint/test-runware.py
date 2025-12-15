from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from PIL import Image
from io import BytesIO
import os
import time
import base64
import uuid
import json
import logging
import requests
import asyncio
from dotenv import load_dotenv
from openai_api_wrapper.example import prompt_enhancer  

load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

OUTPUT_DIR = "/tmp/.temp/txt2poster"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Styles and color schemes data
with open("/home/ai-poster-maker/ai-poster-style-and-color-v2.json", "r") as f:
    STYLES_AND_COLORS_JSON = json.load(f)


class PosterRequest(BaseModel):
    prompt: str
    batch_count: int
    style_id: int
    aspect_ratio: str
    color_id: int
    model_id: int


class PosterResponse(BaseModel):
    status_code: int
    response_message: str
    output_image_urls: List[str]


class ImageGenerationService:
    def __init__(self):
        self.runware_api_key = os.getenv("RUNWARE_API_KEY")
        self.styles = STYLES_AND_COLORS_JSON["style"]
        self.color_schemes = STYLES_AND_COLORS_JSON["color_scheme"]

    def _get_style_by_id(self, style_id: int) -> dict:
        for style in self.styles:
            if style["id"] == style_id:
                return style
        raise ValueError(f"Style with id {style_id} not found")

    def _get_color_scheme_by_id(self, color_id: int) -> dict:
        for color_scheme in self.color_schemes:
            if color_scheme["id"] == color_id:
                return color_scheme
        raise ValueError(f"Color scheme with id {color_id} not found")

    def _build_final_prompt(self, user_prompt: str, style_id: int, color_id: int) -> tuple:
        style = self._get_style_by_id(style_id)
        color_scheme = self._get_color_scheme_by_id(color_id)

        style_details = style.get("prompt", "")  
        color_prompt = color_scheme.get("prompt", "") 
        negative_prompt = style.get("negative_prompt", "")

        structured_prompt = f"""
        You are a creative prompt engineer for an AI-powered poster generation system.

        Your task is to transform user input into a vivid, visually rich, and stylistically coherent prompt suitable for use with an image generation model (e.g., Qwen Image or Stable Diffusion). 
        The output prompt should reflect a strong sense of composition, texture, mood, and visual storytelling — aligned with the provided subject, design style, and color palette.

        ---

        **Subject**:
        {user_prompt}

        **Design Style & Texture Elements**:
        {style_details}

        **Color Palette**:
        {color_prompt}

        ---

        **Instructions**:
        - Begin the prompt with a descriptive scene or subject focus.
        - Weave in the style and texture elements naturally to influence the poster’s mood and layout.
        - Tastefully integrate the given color palette — describe how colors interact with the subject and composition.
        - Mention layout and framing techniques (e.g., circular layout, symmetry, ornamental framing) if applicable.
        - Maintain a creative yet concise tone; avoid redundant phrasing or excessive adjective stacking.
        - Output only the enhanced image-generation prompt. Do not include labels or formatting.

        Respond only with the final descriptive prompt.
        """.strip()

        return structured_prompt, negative_prompt


    async def generate_with_runware(self, request: PosterRequest) -> List[bytes]:
        logger.info("Starting image generation with Runware")

        if not self.runware_api_key:
            raise Exception("Runware API key not configured")

        try:
            from runware import Runware, IImageInference
        except ImportError:
            raise Exception("Runware SDK not installed. Install with: pip install runware")

        structured_prompt, negative_prompt = self._build_final_prompt(
            request.prompt, request.style_id, request.color_id
        ) 

        enhanced_prompt = prompt_enhancer(structured_prompt, negative_prompt)

        width, height = self._get_dimensions_for_aspect_ratio(request.aspect_ratio)

        runware = Runware(api_key=self.runware_api_key)

        try:
            await runware.connect()
            logger.info("Connected to Runware successfully")

            inference_request = IImageInference(
                outputType="base64Data",
                outputFormat="JPG",
                positivePrompt=enhanced_prompt,
                negativePrompt=negative_prompt,
                model="runware:108@1",
                steps=40,
                CFGScale=4,
                width=width,
                height=height,
                numberResults=1,
            )

            logger.info("Generating image with Runware...")
            logger.info(f"Final prompt: {enhanced_prompt}")
            if negative_prompt:
                logger.info(f"Negative prompt: {negative_prompt}")

            b64_object_list = await runware.imageInference(requestImage=inference_request)

            if not b64_object_list or len(b64_object_list) == 0:
                raise Exception("Empty response received from Runware")

            # Extract base64 data and convert to bytes
            image_bytes_list = []
            if hasattr(b64_object_list[0], 'imageBase64Data') and b64_object_list[0].imageBase64Data:
                base64_data = b64_object_list[0].imageBase64Data
                # Remove data URI prefix if present
                if base64_data.startswith('data:image/'):
                    base64_data = base64_data.split(',', 1)[1]
                image_bytes = base64.b64decode(base64_data)
                image_bytes_list.append(image_bytes)
                logger.info("Successfully decoded base64 image data")
            else:
                raise Exception("No base64 image data received from Runware")

            logger.info(f"Successfully generated {len(image_bytes_list)} images with {request.model_id}")
            return image_bytes_list

        except Exception as e:
            logger.error(f"Error during Runware generation: {str(e)}")
            raise
        finally:
            try:
                await runware.disconnect()
                logger.info("Disconnected from Runware")
            except Exception as e:
                logger.warning(f"Error disconnecting from Runware: {e}")

    async def generate_with_flux(self, request: PosterRequest, x_request_id: str,
                                 x_source_environment: str) -> PosterResponse:
        logger.info("Starting image generation with external Flux API")

        external_api_url = os.getenv("FLUX_API_URL")
        if not external_api_url:
            return PosterResponse(
                status_code=500,
                response_message="FLUX_API_URL environment variable not configured",
                output_image_urls=[]
            )

        payload = {
            "prompt": request.prompt,
            "batch_count": request.batch_count,
            "style_id": request.style_id,
            "aspect_ratio": request.aspect_ratio,
            "color_id": request.color_id,
        }

        headers = {
            "X-Request-ID": x_request_id,
            "X-Source-Environment": x_source_environment,
            "Content-Type": "application/json"
        }

        try:
            logger.info(f"Calling external API at {external_api_url}")
            logger.info(f"Final prompt: {request.prompt}")
            response = requests.post(external_api_url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()

            response_data = response.json()

            poster_response = PosterResponse(
                status_code=response_data.get('status_code', 200),
                response_message=response_data.get('response_message', 'Success'),
                output_image_urls=response_data.get('output_image_urls', [])
            )

            logger.info(f"Successfully received response from external API: {poster_response.response_message}")
            return poster_response

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling external API: {str(e)}")
            return PosterResponse(
                status_code=500,
                response_message=f"External API request failed: {str(e)}",
                output_image_urls=[]
            )
        except Exception as e:
            logger.error(f"Error processing external API response: {str(e)}")
            return PosterResponse(
                status_code=500,
                response_message=f"Error processing external API response: {str(e)}",
                output_image_urls=[]
            )

    def _get_dimensions_for_aspect_ratio(self, aspect_ratio: str) -> tuple:
        dimension_map = {
            "1:1": (1024, 1024),
            "16:9": (1344, 768),
            "9:16": (768, 1344),
            "4:3": (1152, 896),
            "3:4": (896, 1152)
        }
        return dimension_map.get(aspect_ratio, (1024, 1024))


def save_generated_images_from_bytes(image_bytes_list: List[bytes], source_env: str) -> List[str]:
    timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")
    saved_files = []

    for i, image_bytes in enumerate(image_bytes_list):
        try:
            image = Image.open(BytesIO(image_bytes))
            filename = f"{source_env}_{timestamp}_{uuid.uuid4().hex[:8]}.jpeg"
            filepath = os.path.join(OUTPUT_DIR, filename)

            # Convert to RGB if necessary (for JPEG)
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')

            image.save(filepath, format="JPEG", quality=85)
            saved_files.append(filename)
            logger.info(f"Saved image {i + 1}: {filename}")

        except Exception as e:
            logger.error(f"Error saving image {i + 1}: {str(e)}")
            raise Exception(f"Failed to save image {i + 1}: {str(e)}")

    return saved_files


image_service = ImageGenerationService()


@app.post("/api/v1/poster-maker/txt2poster", response_model=PosterResponse)
async def generate_poster(
        request: PosterRequest,
        x_request_id: Optional[str] = Header(None, alias="X-Request-ID"),
        x_source_environment: Optional[str] = Header(None, alias="X-Source-Environment"),
):
    if not x_request_id or not x_source_environment:
        raise HTTPException(status_code=400, detail="Missing required headers: X-Request-ID and X-Source-Environment")

    if request.model_id not in [0, 1]:
        raise HTTPException(status_code=400, detail="Model ID must be either 0 or 1")

    logger.info(f"Starting poster generation with Model: {request.model_id}")
    logger.info(f"Request ID: {x_request_id}, Environment: {x_source_environment}")
    logger.info(f"Prompt: {request.prompt[:100]}..." if len(request.prompt) > 100 else f"Prompt: {request.prompt}")
    logger.info(f"Style ID: {request.style_id}, Color ID: {request.color_id}")

    start_time = time.time()

    try:
        if request.model_id == 1:
            image_bytes_list = await image_service.generate_with_runware(request)

            saved_files = save_generated_images_from_bytes(
                image_bytes_list,
                x_source_environment,
            )

            output_urls = [f"/media/txt2poster/{filename}" for filename in saved_files]

            generation_time = time.time() - start_time
            success_message = (
                f"Successfully generated {len(saved_files)} image "
                f"in {generation_time:.2f} seconds"
            )

            return PosterResponse(
                status_code=200,
                response_message=success_message,
                output_image_urls=output_urls
            )
        else:  # flux
            poster_response = await image_service.generate_with_flux(
                request, x_request_id, x_source_environment
            )

            if poster_response.status_code != 200:
                raise HTTPException(
                    status_code=poster_response.status_code,
                    detail=poster_response.response_message
                )

            return poster_response

    except Exception as e:
        error_message = f"Image generation failed: {str(e)}"
        logger.error(error_message)

        raise HTTPException(
            status_code=500,
            detail=error_message
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
