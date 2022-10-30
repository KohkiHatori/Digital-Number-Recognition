from ast import For
from distutils.log import debug
from typing import List
from urllib import response
from fastapi import FastAPI, File, UploadFile, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from predict import Prediction_maker
from starlette.responses import RedirectResponse, FileResponse
from pydantic import BaseModel
import gc
import sys
from PIL import Image
import io
import numpy as np
import cv2
import llib.mmdet_util
import uvicorn
import datetime
import os
sys.path.insert(0, "llib/open_mmlab/mmdetection-2.7.0/build/lib")
from mmdet.apis.inference import init_detector


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

model = None
cls_nms = ["dot"] + [str(x) for x in range(10)]

@app.on_event("startup")
def startup_event():
    global cls_nms
    model_fpath = "../3_model/latest.pth"
    # cfg setting
    mmdet_config_fpath = "llib/open_mmlab/mmdetection-2.7.0/configs/cascade_rcnn/cascade_mask_rcnn_x101_64x4d_fpn_1x_coco.py"
    cfg = llib.mmdet_util.get_base_cfg(mmdet_config_fpath, len(cls_nms))
    # model build
    global model
    model = init_detector(config=cfg, checkpoint=model_fpath, device="cpu")
    gc.collect()

@app.post("/process")
def process_image(files: List[UploadFile] = File(...)):
    global model, cls_nms
    results = {}
    for file in files:
        file_data = file.file.read()
        nparr = np.frombuffer(file_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        pred = Prediction_maker(img, model, cls_nms)
        results.update({file.filename: pred.main()})
    return results

@app.get("/test")
def test():
    return {"message": "test test"}

@app.get("/upload")
def upload(request: Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.get("/fix")
def fix(request: Request):
    return templates.TemplateResponse("via.html", {"request":request})

@app.post("/save_img")
def save_img(files: List[UploadFile] = File(...)):
    for file in files:
        file_data = file.file.read()
        image = Image.open(io.BytesIO(file_data))
        image.save(os.path.join("images", file.filename))
    return "success"
    

@app.post("/save")
def save(file: UploadFile = Form(...)):
    content = str(file.file.read())[2:-1]
    with open (f"data/{datetime.datetime.now()}.json", "w") as f:
        f.write(content)
    return RedirectResponse(url="/upload", status_code=303)

if __name__ == "__main__":
    uvicorn.run("alcohol_api:app", port=8000)
