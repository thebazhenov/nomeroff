# app_nomer.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
from nomeroff_net import pipeline
from nomeroff_net.tools import unzip
from pathlib import Path
from datetime import datetime
import uuid, io, base64, cv2, numpy as np
from PIL import Image
import uvicorn
from uuid import uuid4

app = FastAPI(title="Nomeroff Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
# --- папки ---
STATIC_DIR = Path("static")
RESULTS_DIR = STATIC_DIR / "results"
UPLOADS_DIR = Path("uploads")

STATIC_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Инициализируем пайплайн один раз
nn = pipeline("number_plate_detection_and_reading", image_loader="opencv")  # gpu=True по необходимости

@app.post("/nomer")
async def nomer(file: UploadFile = File(...)):
    raw = await file.read()
    if not raw:
        raise HTTPException(400, "Empty upload")

    # генерим имя (сохраняем расширение)
    stem = f"{datetime.utcnow():%Y%m%d_%H%M%S}_{uuid4().hex}"
    ext = Path(file.filename or "image.jpg").suffix or ".jpg"
    saved_path = (UPLOADS_DIR / f"{stem}{ext}").absolute().as_posix()

    with open(saved_path, "wb") as f:
        f.write(raw)

    try:

        (images, images_bboxs,
         images_points, images_zones, region_ids,
         region_names, count_lines,
         confidences, texts) = unzip(
            nn([saved_path]))

        return {
            "plates": texts
        }
    except Exception as e:
        print(e)
        raise HTTPException(500, f"Nomeroff error: {e}")
    finally:
        await file.close()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)