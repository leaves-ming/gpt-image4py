from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional
import json
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
