from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import health, images

app = FastAPI(title="GPT Image Playground API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(images.router, prefix="/api")

@app.get("/")
async def root():
    return {"code": 0, "message": "GPT Image Playground Backend is running", "docs": "/docs"}
