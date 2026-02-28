# RealityCheck AI – Deepfake Detection System

RealityCheck AI is a real-time deepfake detection system designed to analyze videos and determine whether facial content has been manipulated using artificial intelligence.

With the rise of AI-generated media, distinguishing authentic videos from deepfakes has become increasingly difficult. This project provides a practical and accessible verification tool to improve digital trust.

---

## Key Features

* Video frame extraction
* Face detection from each frame (MTCNN)
* Deepfake classification using Vision Transformer
* Multi-frame result aggregation
* Confidence-based authenticity scoring
* Clear final verdict (Real / Suspicious / Deepfake)
* YouTube Chrome Extension support

---

## How It Works

1. User selects a YouTube video or uploads a video file
2. The system extracts frames from the video
3. Faces are detected in each frame
4. Each detected face is classified as real or manipulated
5. Results from multiple frames are combined
6. A final authenticity score and verdict are generated

---

## Tech Stack

**Backend**

* Python
* Flask / FastAPI

**Deep Learning**

* PyTorch
* Vision Transformer (ViT)
* MTCNN

**Video Processing**

* OpenCV
* NumPy

**Frontend**

* JavaScript
* HTML / CSS (Chrome Extension)

---

## Project Structure

```
RealityCheck/
│── backend/
│── model/
│── extension/
│── utils/
│── app.py
│── requirements.txt
```

---

## How to Run

1. Clone the repository
   git clone [https://github.com/inshirah1243/RealityCheck](https://github.com/inshirah1243/RealityCheck)

2. Install dependencies
   pip install -r requirements.txt

3. Start the backend server
   python app.py

4. Load the Chrome Extension (if included)

5. Upload or analyze a video

---

## Applications

* Media verification
* Misinformation detection
* Identity fraud prevention
* Social media content analysis

---

## Future Enhancements

* Real-time streaming analysis
* Support for more platforms
* Model optimization for faster inference
* Cloud deployment for large-scale usage

---

## Demo

Demo Video: *https://drive.google.com/file/d/1O_naoQHmr1HpevkS0Gw8nxqaE01ZNEfS/view?usp=sharing*

---


If you want, I can also make a slightly more impressive “top section” with badges to make your repo look more serious.
