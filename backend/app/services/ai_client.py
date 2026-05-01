import requests
import itertools
from typing import List, Optional, Dict
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, retry_if_not_exception_type
from requests.exceptions import RequestException, Timeout, ConnectionError, HTTPError
from fastapi import HTTPException
from app.schemas import TaskParams
from app.config import settings
from app.services.image_processor import compress_image, b64_to_bytes, bytes_to_b64

class AIClient:
    def __init__(self, timeout: int = settings.request_timeout):
        self.timeout = timeout
        self.key_pool: List[str] = []
        self.key_cycle = itertools.cycle([])
        self.failed_keys = set()
    
    def update_keys(self, keys: List[str]):
        """更新密钥池，重置轮询器"""
        self.key_pool = [k.strip() for k in keys if k.strip()] if keys else []
        self.failed_keys.clear()
        self.key_cycle = itertools.cycle(self.key_pool)
    
    def get_next_key(self) -> Optional[str]:
        """获取下一个可用密钥"""
        if not self.key_pool:
            return None
        
        # 最多遍历一轮找可用密钥
        for _ in range(len(self.key_pool)):
            key = next(self.key_cycle)
            if key not in self.failed_keys:
                return key
        return None  # 所有密钥都失效

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_not_exception_type(HTTPError) | retry_if_exception_type((Timeout, ConnectionError)) | retry_if_exception_type(HTTPError, lambda e: e.response.status_code not in (401, 403)),
        retry_condition=lambda retry_state: (
            isinstance(retry_state.outcome.exception(), HTTPError) 
            and (500 <= retry_state.outcome.exception().response.status_code < 600 
                 or retry_state.outcome.exception().response.status_code == 429)
        ) if hasattr(retry_state.outcome, 'exception') else True
    )
    def _generate_image_with_key(
        self, 
        prompt: str, 
        params: TaskParams,
        api_path: str,
        api_base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-image-2"
    ) -> List[Dict]:
        """单个密钥的生成请求，带重试逻辑"""
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
        output = []
        for item in result["data"]:
            original = item.get("b64_json") or item.get("url")
            compressed = original
            if params.enable_compress and original.startswith("data:"):
                img_bytes = b64_to_bytes(original)
                compressed_bytes, ext = compress_image(img_bytes)
                compressed = bytes_to_b64(compressed_bytes, ext)
            output.append({
                "original": original,
                "compressed": compressed
            })
        return output

    def generate_image(
        self, 
        prompt: str, 
        params: TaskParams,
        api_path: str,
        api_base_url: Optional[str] = None,
        api_keys: Optional[List[str]] = None,
        model: str = "gpt-image-2"
    ) -> List[Dict]:
        """多密钥轮询生成图片"""
        # 更新密钥池
        self.update_keys(api_keys)
        if not self.key_pool:
            # 没有配置密钥，使用默认配置
            return self._generate_image_with_key(
                prompt=prompt,
                params=params,
                api_path=api_path,
                api_base_url=api_base_url,
                api_key=None,
                model=model
            )
        
        while True:
            current_key = self.get_next_key()
            if not current_key:
                raise HTTPException(status_code=400, detail="所有API密钥均已失效，请检查密钥后重试")
            
            try:
                return self._generate_image_with_key(
                    prompt=prompt,
                    params=params,
                    api_path=api_path,
                    api_base_url=api_base_url,
                    api_key=current_key,
                    model=model
                )
            except HTTPError as e:
                if e.response.status_code in (401, 403):
                    # 标记密钥失效
                    self.failed_keys.add(current_key)
                else:
                    raise e
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
        output = []
        for item in result["data"]:
            original = item.get("b64_json") or item.get("url")
            compressed = original
            if params.enable_compress and original.startswith("data:"):
                img_bytes = b64_to_bytes(original)
                compressed_bytes, ext = compress_image(img_bytes)
                compressed = bytes_to_b64(compressed_bytes, ext)
            output.append({
                "original": original,
                "compressed": compressed
            })
        return output

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_not_exception_type(HTTPError) | retry_if_exception_type((Timeout, ConnectionError)) | retry_if_exception_type(HTTPError, lambda e: e.response.status_code not in (401, 403)),
        retry_condition=lambda retry_state: (
            isinstance(retry_state.outcome.exception(), HTTPError) 
            and (500 <= retry_state.outcome.exception().response.status_code < 600 
                 or retry_state.outcome.exception().response.status_code == 429)
        ) if hasattr(retry_state.outcome, 'exception') else True
    )
    def _edit_image_with_key(
        self, 
        prompt: str, 
        params: TaskParams,
        api_path: str,
        image_files: List,
        api_base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-image-2"
    ) -> List[Dict]:
        """单个密钥的编辑请求，带重试逻辑"""
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
        output = []
        for item in result["data"]:
            original = item.get("b64_json") or item.get("url")
            compressed = original
            if params.enable_compress and original.startswith("data:"):
                img_bytes = b64_to_bytes(original)
                compressed_bytes, ext = compress_image(img_bytes)
                compressed = bytes_to_b64(compressed_bytes, ext)
            output.append({
                "original": original,
                "compressed": compressed
            })
        return output

    def edit_image(
        self, 
        prompt: str, 
        params: TaskParams,
        api_path: str,
        image_files: List,
        api_base_url: Optional[str] = None,
        api_keys: Optional[List[str]] = None,
        model: str = "gpt-image-2"
    ) -> List[Dict]:
        """多密钥轮询编辑图片"""
        # 更新密钥池
        self.update_keys(api_keys)
        if not self.key_pool:
            # 没有配置密钥，使用默认配置
            return self._edit_image_with_key(
                prompt=prompt,
                params=params,
                api_path=api_path,
                image_files=image_files,
                api_base_url=api_base_url,
                api_key=None,
                model=model
            )
        
        while True:
            current_key = self.get_next_key()
            if not current_key:
                raise HTTPException(status_code=400, detail="所有API密钥均已失效，请检查密钥后重试")
            
            try:
                return self._edit_image_with_key(
                    prompt=prompt,
                    params=params,
                    api_path=api_path,
                    image_files=image_files,
                    api_base_url=api_base_url,
                    api_key=current_key,
                    model=model
                )
            except HTTPError as e:
                if e.response.status_code in (401, 403):
                    # 标记密钥失效
                    self.failed_keys.add(current_key)
                else:
                    raise e
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
        output = []
        for item in result["data"]:
            original = item.get("b64_json") or item.get("url")
            compressed = original
            if params.enable_compress and original.startswith("data:"):
                img_bytes = b64_to_bytes(original)
                compressed_bytes, ext = compress_image(img_bytes)
                compressed = bytes_to_b64(compressed_bytes, ext)
            output.append({
                "original": original,
                "compressed": compressed
            })
        return output

ai_client = AIClient()
