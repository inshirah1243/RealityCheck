from fastapi import FastAPI, UploadFile, File
import shutil
import os
from utils import extract_frames
from model import predict_frame
import numpy as np

app = FastAPI()

UPLOAD_FOLDER = "../uploads"
FRAME_FOLDER = "../uploads/frames"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FRAME_FOLDER, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "RealityCheck Backend Running 🚀"}

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        # Extract frames
    frames = extract_frames(file_path, FRAME_FOLDER)

    scores = []
    for frame in frames:
        score = predict_frame(frame)
        scores.append(score)

    final_confidence = float(np.mean(scores))
    stability = float(np.std(scores))

    # Most suspicious frame
    most_suspicious_index = int(np.argmax(scores))
    most_suspicious_score = float(scores[most_suspicious_index])

    # Verdict logic
    if final_confidence < 0.4:
        verdict = "Likely Authentic"
    elif final_confidence < 0.7:
        verdict = "Suspicious"
    else:
        verdict = "Likely Deepfake"

    return {
        "filename": file.filename,
        "frames_extracted": len(frames),
        "frame_scores": scores,
        "final_confidence": final_confidence,
        "stability_score": stability,
        "most_suspicious_frame_index": most_suspicious_index,
        "most_suspicious_score": most_suspicious_score,
        "verdict": verdict
    }