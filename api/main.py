from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, File, UploadFile, HTTPException, status

app = FastAPI()
UPLOAD_DIR = Path("uploads")
ALLOWED = {"image/jpeg", "image/png", "image/webp"}


@app.post("/handler")
async def handler(file: UploadFile = File(...)):
    # 1) Валидация типа
    if file.content_type not in ALLOWED:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Only {sorted(ALLOWED)} are allowed, got {file.content_type!r}",
        )

    # 2) Гарантируем каталог
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # 3) Имя файла (уникализируем, расширение сохраняем)
    suffix = Path(file.filename).suffix or ".bin"
    dest = UPLOAD_DIR / f"{uuid4().hex}{suffix}"

    # 4) Потоковая запись
    chunk_size = 1024 * 1024  # 1 MB
    try:
        with dest.open("wb") as out:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                out.write(chunk)
    finally:
        await file.close()

    return {"saved_as": str(dest), "content_type": file.content_type}
