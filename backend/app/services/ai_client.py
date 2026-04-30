import requests
from typing import List, Optional
from app.schemas import TaskParams
from app.config import settings

class AIClient:
    def __init__(self, timeout: int = settings.request_timeout):
        self.timeout = timeout

    def generate_image(
        self, 
        prompt: str, 
        params: TaskParams,
        api_path: str,
        api_base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-image-2"
    ) -> List[str]:
        """调用文本生图接口，参数全部由前端传入"""
        final_api_key = api_key or settings.default_api_key
        final_base_url = api_base_url or settings.default_api_base_url
        
        if api_path.startswith(("http://", "https://")):
            url = api_path
        else:
            url = f"{final_base_url.rstrip('/')}/{api_path.lstrip('/')}"
        
        headers = {
            "Authorization": f"Bearer {final_api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "model": model,
            "prompt": prompt,
            "size": params.size,
            "quality": params.quality,
            "output_format": params.output_format,
            "moderation": params.moderation,
            "n": params.n
        }
        if params.output_format != "png" and params.output_compression:
            body["output_compression"] = params.output_compression

        response = requests.post(url, headers=headers, json=body, timeout=self.timeout)
        response.raise_for_status()
        result = response.json()
        return [item.get("b64_json") or item.get("url") for item in result["data"]]

    def edit_image(
        self, 
        prompt: str, 
        params: TaskParams,
        api_path: str,
        image_files: List,
        api_base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-image-2"
    ) -> List[str]:
        """调用图片编辑接口，参数全部由前端传入"""
        final_api_key = api_key or settings.default_api_key
        final_base_url = api_base_url or settings.default_api_base_url
        
        if api_path.startswith(("http://", "https://")):
            url = api_path
        else:
            url = f"{final_base_url.rstrip('/')}/{api_path.lstrip('/')}"
        
        headers = {
            "Authorization": f"Bearer {final_api_key}"
        }
        form_data = {
            "model": model,
            "prompt": prompt,
            "size": params.size,
            "quality": params.quality,
            "output_format": params.output_format,
            "moderation": params.moderation
        }
        if params.output_format != "png" and params.output_compression:
            form_data["output_compression"] = str(params.output_compression)

        files = [("image", (f"input_{i}.png", img.file, img.content_type)) for i, img in enumerate(image_files)]
        response = requests.post(url, headers=headers, data=form_data, files=files, timeout=self.timeout)
        response.raise_for_status()
        result = response.json()
        return [item.get("b64_json") or item.get("url") for item in result["data"]]

ai_client = AIClient()
