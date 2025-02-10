from pydantic import BaseModel
from typing import List, Optional

class DecryptRequest(BaseModel):
    url: str
    mediaKey: str = None
    mimetype: str

class RunData(BaseModel):
    thread_id: str
    run_id: str

class TextFormatRequest(BaseModel):
    text: str

class TextFormatResponse(BaseModel):
    formatted_text: str

class CrawlRequest(BaseModel):
    base_url: str
    country_code: str
    language_code: str
    webhook: str

class PhoneNumberRequest(BaseModel):
    phone_number: str

class CountryCodeResponse(BaseModel):
    country_code: str
    national_number: int
    carrier: Optional[str]
    time_zones: List[str]
