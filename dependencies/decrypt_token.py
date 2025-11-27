from base64 import b64decode
from typing import Optional
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DecryptToken:
    """
    Replicates the DecryptionAlgo Swift class logic in Python.
    Handles a custom "garbage removal" step, AES-256-CBC decryption,
    and a custom value extraction process.
    """

    _SHARED_SECRET_KEY = "!.z4@B9Y,A1&+LO?12Y4*/x8I0^S)4Kr".encode("utf-8")
    _IV = "stwx8Yi'CvkL{}-+".encode("utf-8")
    _VALUES_OF_CHARACTER = {
        "a": 0,
        "!": 1,
        "y": 2,
        ",": 3,
        "s": 4,
        "r": 5,
        "?": 6,
        "T": 7,
        "V": 8,
        "p": 9,
    }

    def validate(self, key: str, allowed_diff: int = 60 * 60) -> bool:
        """
        :param allowed_diff: the key is a time, it can be from past with `allowe_diff` amount
        """
        return True

    def decrypt(self, key: str) -> int | None:
        """
        The main decryption function.

        :param key: The raw string containing encrypted text plus 'garbage' characters.
        :return: The final decrypted and processed integer value, or None on failure.
        """
        try:
            encrypted_b64 = self._get_encrypted_dynamic_text(key=key)
            encrypted_data = b64decode(encrypted_b64)

            decrypted_bytes = self._crypt(data=encrypted_data)
            if not decrypted_bytes:
                logger.info("Decryption Failed")
                return None

            dynamic_text = decrypted_bytes.decode("utf-8")

            actual_value = self._get_actual_value(from_text=dynamic_text)
            return actual_value

        except Exception as e:
            logger.info(msg=f"An error occurred during decryption: {e}")
            return None

    def _get_encrypted_dynamic_text(self, key: str) -> str:
        """
        Filters the input key string to remove 'garbage' characters
        based on a complex, oscillating interval pattern.
        """
        should_increase_garbage = True
        lowest_garbage_no = 4
        highest_garbage_no = 10
        no_of_garbage = highest_garbage_no
        final_key = ""
        ignore_index = 0

        for single_character in key:
            if ignore_index < no_of_garbage:
                ignore_index += 1
                continue

            final_key += single_character
            ignore_index = 0

            if should_increase_garbage:
                no_of_garbage += 1
            else:
                no_of_garbage -= 1

            if no_of_garbage == highest_garbage_no:
                should_increase_garbage = False
            elif no_of_garbage == lowest_garbage_no:
                should_increase_garbage = True

        return final_key

    def _crypt(self, data: bytes) -> Optional[bytes]:
        """
        Performs AES-256-CBC decryption with PKCS7 padding.

        :param data: The encrypted bytes.
        :return: The decrypted bytes, or None on failure.
        """
        try:
            cipher = Cipher(
                algorithms.AES(self._SHARED_SECRET_KEY),
                modes.CBC(self._IV),
                backend=default_backend(),
            )

            decryptor = cipher.decryptor()

            decrypted_data = decryptor.update(data) + decryptor.finalize()
            return decrypted_data

        except Exception as e:
            print(f"Decryption error (AES-CBC): {e}")
            return None

    def _get_actual_value(self, from_text: str) -> int:
        """
        Extracts numerical digits from the dynamic text string
        based on the custom character-to-digit map and interleaving logic.
        """
        prefix_text = []
        suffix_text = []

        text_length = len(from_text)
        actual_text_length = text_length // 3
        prefix_length = (actual_text_length + 1) // 2

        prefix_taken = 0
        for index, single_character in enumerate(from_text):
            if index % 3 != 0:
                continue

            char_str = single_character

            if prefix_taken < prefix_length:
                prefix_text.append(char_str)
                prefix_taken += 1
            else:
                suffix_text.append(char_str)

        final_value = 0
        no_of_zero_prefix = 0

        for i, p_char in enumerate(prefix_text):
            p_digit = self._VALUES_OF_CHARACTER.get(p_char, 0)
            final_value = (final_value * 10) + p_digit

            if final_value == 0 and p_digit == 0:
                no_of_zero_prefix += 1

            if i < len(suffix_text):
                s_char = suffix_text[i]
                s_digit = self._VALUES_OF_CHARACTER.get(s_char, 0)
                final_value = (final_value * 10) + s_digit

                if final_value == 0 and s_digit == 0:
                    no_of_zero_prefix += 1

        actual_value = 0
        temp_value = final_value

        while temp_value > 0:
            actual_value = (actual_value * 10) + (temp_value % 10)
            temp_value //= 10

        if final_value == 0:
            return 0

        if no_of_zero_prefix > 0:
            for _ in range(no_of_zero_prefix):
                actual_value *= 10

        return actual_value


# algo = DecryptionAlgo()
# # Replace 'YOUR_ENCRYPTED_KEY_STRING' with an actual string processed by the Swift encryption
# # result = algo.decrypt(key='YOUR_ENCRYPTED_KEY_STRING')
# # print(f"\nFinal Decrypted Value: {result}")
