import asyncio
import os
import aiohttp
import base64
import json
import httpx
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Depends, APIRouter, BackgroundTasks
from typing import List
from api.dependencies import get_http_client
from services.external_services import client
from auth.auth import refresh_access_token, get_credentials, is_token_expired
from services.external_services import aromachat, brasil_living_kit
from services.rastreio_service import rastreio
from services.crawl_service import start_crawling
from services.phone_service import get_phone_number_details
from utils.media_utils import decrypt_media, transcribe_audio
from utils.utils import cleanup_audio_files, md_to_whatsapp_md
from schemas.schemas import DecryptRequest, RunData, TextFormatRequest, TextFormatResponse, CrawlRequest, PhoneNumberRequest, CountryCodeResponse
from config import AUDIO_FILES_DIR, TOKEN_DIR_PATH

router = APIRouter()

@router.post("/decrypt")
async def decrypt_endpoint(decrypt_request: DecryptRequest, http_client=Depends(get_http_client)):
    # Determine media type based on mimetype
    if decrypt_request.mimetype.startswith('audio/'):
        media_type = 'Audio'
    elif decrypt_request.mimetype.startswith('image/'):
        media_type = 'Image'
    else:
        raise HTTPException(status_code=400, detail='Unsupported media type')

    decrypted_data = await decrypt_media(decrypt_request.url, decrypt_request.mediaKey, media_type)

    if media_type == 'Audio':
        filepath = os.path.join(AUDIO_FILES_DIR, base64.urlsafe_b64encode(os.urandom(16)).decode('utf-8') + '.ogg')
        with open(filepath, 'wb') as audio_file:
            audio_file.write(decrypted_data)

        transcription = await transcribe_audio(filepath, decrypt_request.mimetype)
        os.remove(filepath)  # Clean up the audio file after transcription
        await cleanup_audio_files()
        return {"transcription": transcription}
    elif media_type == 'Image':
        base64_decrypted_data = base64.b64encode(decrypted_data).decode('utf-8')
        return {"base64": base64_decrypted_data}

# Additional routes...
