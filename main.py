# framework
from fastapi import FastAPI, File, UploadFile
import asyncio
# face comparison
from insightface import compare_two_faces
import numpy as np
import cv2

app = FastAPI()


@app.get("/health")
async def confirm_health():
    return {"status": "I'm still alive..."}


@app.post("/compare/")
async def compare_faces(face1: UploadFile = File(...), face2: UploadFile = File(...)):
    # for concurrency
    # `create_task` is only for Python 3.7+
    # `ensure_future` is its alternative
    get_face1_bytes_task = asyncio.ensure_future(face1.read())
    get_face2_bytes_task = asyncio.ensure_future(face2.read())
    face1_bytes = await get_face1_bytes_task
    face2_bytes = await get_face2_bytes_task
    # convert to cv2 array
    img_np_arr = np.frombuffer(face1_bytes, np.uint8)
    f1 = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)
    img_np_arr = np.frombuffer(face2_bytes, np.uint8)
    f2 = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)
    # compare
    sim, dist = compare_two_faces(f1, f2)
    # convert to NORMAL float from `numpy.float32`
    return {'sim': float(sim), 'dist': float(dist)}
