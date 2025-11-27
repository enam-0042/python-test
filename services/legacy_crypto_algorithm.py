import random
from base64 import b64encode, b64decode
from datetime import datetime, timezone
from typing import Optional

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class LegacyCryptoAlgorithm:
    _SHARED_SECRET_KEY = "!.z4@B9Y,A1&+LO?12Y4*/x8I0^S)4Kr".encode('utf-8')
    _IV = "stwx8Yi'CvkL{}-+".encode('utf-8') # noqa


    _VALUES_OF_INT = {
        0: "a", 1: "!", 2: "y", 3: ",", 4: "s",
        5: "r", 6: "?", 7: "T", 8: "V", 9: "p"
    }

    _VALUES_OF_CHARACTER = {v: k for k, v in _VALUES_OF_INT.items()}

    _ALL_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789,.;:{}()-_+=|" # noqa

    def __init__(self):
        self._SHARED_SECRET_KEY_STR = self._SHARED_SECRET_KEY.decode('utf-8')
        self._ALL_CHARS_LIST = list(self._ALL_CHARACTERS)

    def encrypt(self) -> Optional[str]:
        """
        Generates a new encryption key based on the current timestamp in milliseconds
        """
        try:
            dynamic_text = self._create_dynamic_text()

            encrypted_bytes = self._crypt_aes(dynamic_text.encode('utf-8'), is_encrypt=True)
            if not encrypted_bytes:
                return None

            base64_string = b64encode(encrypted_bytes).decode('utf-8')

            final_key = self._extended_api_key(base64_string)
            return final_key

        except Exception as e:
            print(f"Encryption Error: {e}")
            return None

    def decrypt(self, key: str) -> Optional[int]:
        """
        Decrypts a dynamic API key back to the timestamp integer. milliseconds
        """
        try:
            clean_base64 = self._remove_garbage_from_key(key)

            encrypted_data = b64decode(clean_base64)
            decrypted_bytes = self._crypt_aes(encrypted_data, is_encrypt=False)

            if not decrypted_bytes:
                return None

            dynamic_text = decrypted_bytes.decode('utf-8')

            actual_value = self._get_actual_value(dynamic_text)
            return actual_value

        except Exception as e:
            print(f"Decryption Error: {e}")
            return None

    def _create_dynamic_text(self) -> str:
        """
        Generates the scrambled string from current time.
        Logic: Takes reversed time digits, splits them into prefix/suffix,
        and inserts random noise.
        """
        # timeinterval since: timeIntervalSince1970 * 1000
        # time_interval_int = int(time.time() * 1000)
        time_interval_int = int(datetime.now(timezone.utc).timestamp() * 1000)
        prefix_text = ""
        suffix_text = ""
        prefix_taken = 0
        suffix_taken = 0

        while time_interval_int > 0:
            last_digit = time_interval_int % 10

            # Default chars 's' or 'i' if key lookup fails (mimicking Swift ?? logic)
            default_char = "i" if prefix_taken > suffix_taken else "s"
            encrypted_char = self._VALUES_OF_INT.get(last_digit, default_char)

            if prefix_taken > suffix_taken:
                suffix_taken += 1
                suffix_text += encrypted_char
                suffix_text += (self._get_random_secret_char() + self._get_random_hash_char())
            else:
                prefix_taken += 1
                prefix_text += encrypted_char
                prefix_text += (self._get_random_hash_char() + self._get_random_secret_char())

            time_interval_int //= 10

        return prefix_text + suffix_text

    def _extended_api_key(self, key: str) -> str:
        """
        Adds garbage characters.
        """
        should_increase = True
        lowest_garbage = 4
        highest_garbage = 10
        no_of_garbage = highest_garbage  # Starts at 10

        final_key = ""

        for char in key:
            for _ in range(no_of_garbage):
                final_key += random.choice(self._ALL_CHARS_LIST)

            final_key += char

            if should_increase:
                no_of_garbage += 1
            else:
                no_of_garbage -= 1

            if no_of_garbage == highest_garbage:
                should_increase = False
            elif no_of_garbage == lowest_garbage:
                should_increase = True

        return final_key

    @staticmethod
    def _remove_garbage_from_key(key: str) -> str:
        """
        Removes garbage characters.
        """
        should_increase = True
        lowest_garbage = 4
        highest_garbage = 10
        no_of_garbage = highest_garbage

        final_key = ""
        skip_counter = 0

        for char in key:
            if skip_counter < no_of_garbage:
                skip_counter += 1
                continue

            final_key += char
            skip_counter = 0

            if should_increase:
                no_of_garbage += 1
            else:
                no_of_garbage -= 1

            if no_of_garbage == highest_garbage:
                should_increase = False
            elif no_of_garbage == lowest_garbage:
                should_increase = True

        return final_key

    def _get_actual_value(self, text: str) -> int:
        """
        Reconstructs the integer from the scrambled text.
        """
        prefix_chars = []
        suffix_chars = []

        total_len = len(text)
        data_len = total_len // 3
        prefix_len = (data_len + 1) // 2

        prefix_taken = 0

        for i, char in enumerate(text):
            if i % 3 != 0: continue

            if prefix_taken < prefix_len:
                prefix_chars.append(char)
                prefix_taken += 1
            else:
                suffix_chars.append(char)

        final_val = 0
        zeros_count = 0

        for i, p_char in enumerate(prefix_chars):
            digit = self._VALUES_OF_CHARACTER.get(p_char, 0)
            final_val = (final_val * 10) + digit
            if final_val == 0: zeros_count += 1

            if i < len(suffix_chars):
                digit = self._VALUES_OF_CHARACTER.get(suffix_chars[i], 0)
                final_val = (final_val * 10) + digit
                if final_val == 0: zeros_count += 1

        actual_val = 0
        temp = final_val

        while temp > 0:
            actual_val = (actual_val * 10) + (temp % 10)
            temp //= 10

        if final_val == 0: return 0

        for _ in range(zeros_count):
            actual_val *= 10

        return actual_val


    def _crypt_aes(self, data: bytes, is_encrypt: bool) -> Optional[bytes]:
        """Standard AES-256-CBC with PKCS7 Padding"""
        try:
            cipher = Cipher(
                algorithms.AES(self._SHARED_SECRET_KEY),
                modes.CBC(self._IV),
                backend=default_backend()
            )

            if is_encrypt:
                padding_adder = padding.PKCS7(128).padder()
                padded_data = padding_adder.update(data) + padding_adder.finalize()
                encryptor = cipher.encryptor()
                return encryptor.update(padded_data) + encryptor.finalize()
            else:
                decryptor = cipher.decryptor()
                decrypted_padded = decryptor.update(data) + decryptor.finalize()
                unpading_adder = padding.PKCS7(128).unpadder()
                return unpading_adder.update(decrypted_padded) + unpading_adder.finalize()
        except Exception:
            return None

    def _get_random_secret_char(self) -> str:
        return random.choice(self._SHARED_SECRET_KEY_STR)

    def _get_random_hash_char(self) -> str:
        return random.choice(list(self._VALUES_OF_INT.values()))