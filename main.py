from fastapi import FastAPI
import shutil
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Разрешить все источники
    allow_credentials=True,        # Разрешить передачу куки и авторизационных заголовков
    allow_methods=["*"],           # Разрешить все HTTP методы
    allow_headers=["*"],           # Разрешить все заголовки
)

@app.post("/")
async def upload_image(image: UploadFile = File(...)):
    file_path = "tmp/img.jpg"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
        
    return [1,2]
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)