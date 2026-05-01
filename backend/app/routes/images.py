from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import List, Optional
import json
import zipfile
import tempfile
import os
import requests
import base64
from app.schemas import ImageGenerationRequest, TaskParams
from app.services.ai_client import ai_client

router = APIRouter(prefix="/images")

@router.post("/generate")
async def generate_image(request: ImageGenerationRequest):
    try:
        images = ai_client.generate_image(
            prompt=request.prompt,
            params=request.params,
            api_base_url=request.api_base_url,
            api_path=request.api_path,
            api_key=request.api_key,
            model=request.model
        )
        return {"code": 0, "message": "success", "data": {"images": images}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/edit")
async def edit_image(
    prompt: str = Form(...),
    params: str = Form(...),
    api_base_url: Optional[str] = Form(None),
    api_path: str = Form(...),
    api_key: Optional[str] = Form(None),
    model: str = Form("gpt-image-2"),
    images: List[UploadFile] = File(...)
):
    try:
        task_params = TaskParams(**json.loads(params))
        images_result = ai_client.edit_image(
            prompt=prompt,
            params=task_params,
            api_base_url=api_base_url,
            api_path=api_path,
            api_key=api_key,
            image_files=images,
            model=model
        )
        return {"code": 0, "message": "success", "data": {"images": images_result}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch-download")
async def batch_download(image_urls: list[str]):
    if len(image_urls) > 50:
        raise HTTPException(status_code=400, detail="最多支持50张图片批量打包")
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "ai_images.zip")
        
        # 打包ZIP
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for idx, img_data in enumerate(image_urls):
                try:
                    if img_data.startswith("data:"):
                        # 处理base64图片
                        b64_str = img_data.split(",")[1]
                        ext = img_data.split(";")[0].split("/")[1]
                        content = base64.b64decode(b64_str)
                        zipf.writestr(f"image_{idx+1}.{ext}", content)
                    else:
                        # 处理URL图片
                        response = requests.get(img_data, timeout=10)
                        response.raise_for_status()
                        ext = response.headers.get("content-type", "image/png").split("/")[1]
                        zipf.writestr(f"image_{idx+1}.{ext}", response.content)
                except Exception as e:
                    # 跳过下载失败的图片
                    continue
        
        # 返回文件流供前端下载
        return FileResponse(zip_path, filename="ai_images.zip", media_type="application/zip")
