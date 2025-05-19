from fastapi import FastAPI
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import io
from fastapi.staticfiles import StaticFiles
from fastapi import HTTPException


from huggingface_hub import hf_hub_download
from ultralytics import YOLO
from supervision import Detections
from PIL import Image
import random



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Разрешить все источники
    allow_credentials=True,        # Разрешить передачу куки и авторизационных заголовков
    allow_methods=["*"],           # Разрешить все HTTP методы
    allow_headers=["*"],           # Разрешить все заголовки
)


def getFaceHeight(img):
  model_path = hf_hub_download(repo_id="arnabdhar/YOLOv8-Face-Detection", filename="model.pt")
  model1 = YOLO(model_path)
#   output = model1(Image.open(img))
  output = model1(img)
  results = Detections.from_ultralytics(output[0])
  if (len(results) == 0):
    raise HTTPException(status_code=510)
  x_min, y_min, x_max, y_max = results.xyxy[0]
  return [y_max - y_min, x_max-x_min]

def getHeight(img): 
  model_path = hf_hub_download(
      repo_id = "pitangent-ds/YOLOv8-human-detection-thermal",
      filename = "model.pt"
  )
  model = YOLO(model_path)
  model_output = model(img, conf=0.6, verbose=False)
  results = Detections.from_ultralytics(model_output[0])
  if (len(results) == 0):
     raise HTTPException(status_code=510)
  x_min, y_min, x_max, y_max = results.xyxy[0]
#   height = y_max - y_min
  return [y_max - y_min, x_max - x_min]


async def neuro(img): 
    image_data = await img.read()
    img = Image.open(io.BytesIO(image_data)).convert("RGB")
    face_height, face_width = getFaceHeight(img)
    height_px, body_width = getHeight(img)
    face_base = 23
    height = int(height_px / face_height * face_base)
    normal_scale = 3.2
    ratio = body_width / face_width
    if ratio > normal_scale:
        weight = (height % 100) + 10  # если тело широкое — прибавляем
    elif ratio == normal_scale:
        weight = (height % 100)
    else:
        weight = (height % 100) - 10  # если узкое — убавляем

    return weight, height

@app.post("/api/neuro/")
async def upload_image(image: UploadFile = File(...)):
    return await neuro(image)

app.mount("/", StaticFiles(directory="browser", html=True))

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000,)
