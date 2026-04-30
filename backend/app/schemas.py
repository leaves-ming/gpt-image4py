from pydantic import BaseModel
from typing import Optional, List, Literal

class TaskParams(BaseModel):
    size: str
    quality: Literal['auto', 'low', 'medium', 'high']
    output_format: Literal['png', 'jpeg', 'webp']
    output_compression: Optional[int] = None
    moderation: Literal['auto', 'low']
    n: int = 1

class ImageGenerationRequest(BaseModel):
    prompt: str
    params: TaskParams
    api_base_url: Optional[str] = None
    api_path: str
    api_key: Optional[str] = None
    model: str = "gpt-image-2"
    input_images: Optional[List[str]] = None
