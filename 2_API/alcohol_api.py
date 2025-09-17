"""
Alcohol Detection ML System - FastAPI Backend

This module provides a FastAPI-based web service for automated alcohol level detection
from digital display images. It includes endpoints for image upload, processing,
and annotation correction.

Developed during ML engineering internship at Second Xight Analytica, Tokyo (2022)
for transportation safety compliance automation.
"""

from typing import List
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


# Initialize FastAPI application
app = FastAPI(
    title="Alcohol Detection ML System",
    description="Automated alcohol level detection from digital display images",
    version="1.0.0"
)

# Template and static file configuration
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global model variables
model = None  # Cascade R-CNN model for digit detection
cls_nms = ["dot"] + [str(x) for x in range(10)]  # Class names: [".", "0", "1", ..., "9"]

@app.on_event("startup")
def startup_event():
    """
    Initialize the ML model on application startup.

    Loads the trained Cascade R-CNN model for digit detection from alcohol
    detector displays. The model is configured to detect digits (0-9) and
    decimal points from digital display images.
    """
    global cls_nms, model

    # Model file path (excluded from repository due to size)
    model_fpath = "../3_model/latest.pth"

    # MMDetection configuration for Cascade R-CNN with ResNeXt-101 backbone
    mmdet_config_fpath = "llib/open_mmlab/mmdetection-2.7.0/configs/cascade_rcnn/cascade_mask_rcnn_x101_64x4d_fpn_1x_coco.py"

    # Build model configuration
    cfg = llib.mmdet_util.get_base_cfg(mmdet_config_fpath, len(cls_nms))

    # Initialize the detector model
    model = init_detector(config=cfg, checkpoint=model_fpath, device="cpu")

    # Clean up memory
    gc.collect()

@app.post("/process")
def process_image(files: List[UploadFile] = File(...)):
    """
    Process uploaded images to detect and read digital numbers.

    Args:
        files: List of uploaded image files

    Returns:
        dict: Dictionary mapping filenames to detected number strings
    """
    global model, cls_nms
    results = {}

    for file in files:
        # Read uploaded file data
        file_data = file.file.read()

        # Convert to OpenCV image format
        nparr = np.frombuffer(file_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Run ML model prediction
        pred = Prediction_maker(img, model, cls_nms)
        results.update({file.filename: pred.main()})

    return results

@app.get("/test")
def test():
    return {"message": "test test"}

@app.get("/upload")
def upload(request: Request):
    """
    Serve the main image upload interface.

    Returns:
        HTML template for drag-and-drop image upload
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/save_img")
def save_img(files: List[UploadFile] = File(...)):
    """
    Save uploaded images to the local images directory.

    Args:
        files: List of uploaded image files

    Returns:
        str: Success confirmation message
    """
    for file in files:
        # Read and save each uploaded file
        file_data = file.file.read()
        image = Image.open(io.BytesIO(file_data))
        image.save(os.path.join("images", file.filename))

    return "success"



if __name__ == "__main__":
    uvicorn.run("alcohol_api:app", port=8000)
