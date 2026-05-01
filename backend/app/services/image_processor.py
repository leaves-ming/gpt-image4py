from PIL import Image
import io
import base64
from typing import Union, Tuple

def compress_image(image_content: bytes, quality: int = 85, max_dimension: int = 2048) -> Tuple[bytes, str]:
    """
    压缩图片：保持宽高比，最大边长不超过2048px，质量85%
    返回压缩后的内容和文件扩展名
    """
    img = Image.open(io.BytesIO(image_content))
    format = img.format
    
    # 等比例缩放
    width, height = img.size
    if max(width, height) > max_dimension:
        scale = max_dimension / max(width, height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # 压缩保存
    output = io.BytesIO()
    if img.mode == "RGBA":
        ext = "png"
        img.save(output, format="PNG", quality=quality, optimize=True)
    else:
        ext = "jpg"
        img.save(output, format="JPEG", quality=quality, optimize=True)
    
    return output.getvalue(), ext

def b64_to_bytes(b64_str: str) -> bytes:
    """base64字符串转bytes"""
    if b64_str.startswith("data:"):
        b64_str = b64_str.split(",")[1]
    return base64.b64decode(b64_str)

def bytes_to_b64(content: bytes, ext: str) -> str:
    """bytes转base64字符串"""
    b64 = base64.b64encode(content).decode("utf-8")
    mime = "image/png" if ext == "png" else "image/jpeg"
    return f"data:{mime};base64,{b64}"
