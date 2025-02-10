import io
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Hash import HMAC, SHA256
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from pydub import AudioSegment
from speech_recognition import Recognizer, AudioFile
from api.dependencies import get_http_client

# Define any MIME type mappings and constants for media processing
MEDIA_TYPE_MAPPING = {
    'audio/3gpp': 'Audio',
    'audio/aac': 'Audio',
    'audio/aiff': 'Audio',
    'audio/amr': 'Audio',
    'audio/mp4': 'Audio',
    'audio/mpeg': 'Audio',
    'audio/ogg; codecs=opus': 'Audio',
    'audio/qcelp': 'Audio',
    'audio/wav': 'Audio',
    'audio/webm': 'Audio',
    'audio/x-caf': 'Audio',
    'audio/x-ms-wma': 'Audio',
    'audio/ogg': 'Audio',
    'image/gif': 'Image',
    'image/jpeg': 'Image',
    'image/png': 'Image',
    'video/3gpp': 'Video',
    'video/avi': 'Video',
    'video/mp4': 'Video',
    'video/mpeg': 'Video',
    'video/quicktime': 'Video',
    'video/x-flv': 'Video',
    'video/x-ms-asf': 'Video',
}

# Decrypts multimedia using WhatsApp's encryption algorithm
async def decrypt_media(media_url: str, media_key_encoded: str, media_type: str) -> bytes:
    media_key = base64.b64decode(media_key_encoded)
    salt = b'\0' * 32
    info = f'WhatsApp {media_type} Keys'.encode()
    backend = default_backend()
    hkdf = HKDF(algorithm=hashes.SHA256(), length=112, salt=salt, info=info, backend=backend)
    media_key_expanded = hkdf.derive(media_key)
    iv = media_key_expanded[:16]
    cipher_key = media_key_expanded[16:48]
    mac_key = media_key_expanded[48:80]

    client = await get_http_client(timeout=30.0)
    try:
        async with client:
            response = await client.get(media_url)
            response.raise_for_status()
            media_data = response.content
            file_data = media_data[:-10]
            file_mac = media_data[-10:]
            hmac_calculated = HMAC.new(mac_key, msg=iv + file_data, digestmod=SHA256).digest()[:10]
            if hmac_calculated != file_mac:
                raise ValueError('MAC validation failed')
            decryptor = AES.new(cipher_key, AES.MODE_CBC, iv)
            decrypted_data = unpad(decryptor.decrypt(file_data), AES.block_size)
            print(f"{media_type.capitalize()} Base64 Decryption succeeded!")
            return decrypted_data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise
    finally:
        await client.aclose()  # Make sure to close the client

# Additional utility functions...
