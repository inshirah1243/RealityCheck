import os
import shutil
import cv2
import yt_dlp
import numpy as np

from fastapi import FastAPI, UploadFile, File, Body
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from facenet_pytorch import MTCNN
from PIL import Image

from model import predict_frame

app = FastAPI()

# ===============================
# CORS
# ===============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================
# BASE DIRECTORIES
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
FRAMES_FOLDER = os.path.join(BASE_DIR, "frames")
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FRAMES_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ===============================
# FACE DETECTOR
# ===============================
mtcnn = MTCNN(keep_all=True)

def extract_faces_from_frame(frame):
    img = Image.fromarray(frame)
    boxes, _ = mtcnn.detect(img)

    faces = []

    if boxes is not None:
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)

            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(frame.shape[1], x2)
            y2 = min(frame.shape[0], y2)

            face = frame[y1:y2, x1:x2]

            if face.size > 0:
                faces.append(face)

    return faces


# ===============================
# FRAME EXTRACTION
# ===============================
def extract_frames(video_path, output_folder):

    for f in os.listdir(output_folder):
        os.remove(os.path.join(output_folder, f))

    cap = cv2.VideoCapture(video_path)
    count = 0
    frame_paths = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % 30 == 0:
            frame_path = os.path.join(output_folder, f"frame_{count}.jpg")
            cv2.imwrite(frame_path, frame)
            frame_paths.append(frame_path)

        count += 1

    cap.release()
    return frame_paths


# ===============================
# CORE ANALYSIS LOGIC (UPDATED)
# ===============================
def analyze_video(video_path):

    frame_paths = extract_frames(video_path, FRAMES_FOLDER)

    if not frame_paths:
        return None, "No frames extracted"

    scores = []
    fake_count = 0
    total_faces = 0

    # 🔥 Adjustable per-face threshold
    PER_FACE_THRESHOLD = 0.65

    for frame_path in frame_paths:
        frame = cv2.imread(frame_path)

        if frame is None:
            continue

        faces = extract_faces_from_frame(frame)

        for face in faces:
            score = predict_frame(face)
            scores.append(score)
            total_faces += 1

            if score > PER_FACE_THRESHOLD:
                fake_count += 1

    if total_faces == 0:
        return None, "No faces detected"

    fake_ratio = fake_count / total_faces
    average_confidence = sum(scores) / len(scores)
    stability_score = max(scores) - min(scores)

    return {
        "faces_analyzed": total_faces,
        "fake_ratio": fake_ratio,
        "average_confidence": average_confidence,
        "stability_score": stability_score
    }, None


# ===============================
# FILE UPLOAD ENDPOINT
# ===============================
@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):

    video_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result, error = analyze_video(video_path)

    if error:
        return JSONResponse({"error": error}, status_code=400)

    return {
        "filename": file.filename,
        **result
    }


# ===============================
# YOUTUBE ANALYSIS ENDPOINT
# ===============================
@app.post("/analyze_youtube/")
async def analyze_youtube(data: dict = Body(...)):

    url = data.get("url")
    if not url:
        return JSONResponse({"error": "No URL provided"}, status_code=400)

    ydl_opts = {
        "format": "18",
        "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(id)s.%(ext)s"),
        "quiet": False,
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

    if not os.path.exists(filename):
        return JSONResponse({"error": "Downloaded file not found"}, status_code=500)

    result, error = analyze_video(filename)

    if error:
        return JSONResponse({"error": error}, status_code=400)

    return result


# ===============================
# STATIC FILES
# ===============================
app.mount("/frames", StaticFiles(directory=FRAMES_FOLDER), name="frames")
app.mount("/", StaticFiles(directory=os.path.join(BASE_DIR, "frontend"), html=True), name="frontend")