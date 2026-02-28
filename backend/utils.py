import cv2
import os

def extract_frames(video_path, output_folder, num_frames=8):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        return []

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]
    
    os.makedirs(output_folder, exist_ok=True)

    saved_frames = []

    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            frame_filename = os.path.join(output_folder, f"frame_{idx}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frames.append(frame_filename)

    cap.release()
    return saved_frames