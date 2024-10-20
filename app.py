from flask import Flask, request, jsonify
import os
import cv2
import glob
from deepface import DeepFace
from werkzeug.utils import secure_filename
import numpy as np
from subprocess import run


app = Flask(__name__)

# Create upload and frames directory
UPLOAD_FOLDER = 'uploads'
FRAMES_FOLDER = 'frames'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FRAMES_FOLDER, exist_ok=True)


@app.route('/analyze-video', methods=['POST'])
def analyze_video():
    if 'file' not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file provided",
            "data": None
        }), 400

    video_file = request.files['file']
    video_filename = secure_filename(video_file.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    video_file.save(video_path)

    try:
        # Step 1: Extract frames from the video
        frames_folder = extract_frames(video_path)

        # Step 2: Analyze the frames for emotions
        emotion_data = analyze_emotions(frames_folder)

        # Step 3: Aggregate emotion results
        averaged_emotions = aggregate_emotions(emotion_data)

        # Clean up files after processing
        clean_up(video_path, frames_folder)

        # Return the response in the desired format
        return jsonify({
            "status": "success",
            "message": "Video analysis completed successfully",
            "data": {
                "averaged_emotions": averaged_emotions
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred during video analysis: {str(e)}",
            "data": None
        }), 500



@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API works"})


def extract_frames(video_path):
    frames_folder = os.path.join(FRAMES_FOLDER, os.path.basename(video_path).split('.')[0])
    os.makedirs(frames_folder, exist_ok=True)

    # Extract 1 frame per second using ffmpeg
    command = f"ffmpeg -i {video_path} -vf format=yuv420p,fps=1 {frames_folder}/frame_%04d.jpg"
    # command = f"ffmpeg -i {video_path} -vf fps=1 {frames_folder}/frame_%04d.jpg"
    # run(command, shell=True)
    result = run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
    
    return frames_folder

def analyze_emotions(frames_folder):
    results = []

    for frame_path in glob.glob(f"{frames_folder}/*.jpg"):
        try:
            # Analyze the frame using DeepFace's emotion model
            analysis = DeepFace.analyze(img_path=frame_path, actions=['emotion'])

            # Ensure analysis is a list and access the first element
            if isinstance(analysis, list) and len(analysis) > 0:
                emotions = analysis[0]['emotion']  # Access the 'emotion' data from the first dictionary
                results.append({
                    "frame": frame_path,
                    "emotions": emotions
                })
            else:
                print(f"Unexpected analysis structure for {frame_path}: {analysis}")

        except Exception as e:
            print(f"Error analyzing {frame_path}: {e}")

    return results


def aggregate_emotions(emotion_data):
    # If no frames were processed, return an empty result
    if not emotion_data:
        return {}

    emotion_keys = emotion_data[0]['emotions'].keys()
    aggregated_emotions = {key: [] for key in emotion_keys}

    # Aggregate emotion scores for each frame
    for data in emotion_data:
        for emotion, score in data['emotions'].items():
            aggregated_emotions[emotion].append(score)

    # Calculate the average for each emotion
    averaged_emotions = {emotion: np.mean(scores) for emotion, scores in aggregated_emotions.items()}

    return averaged_emotions

def clean_up(video_path, frames_folder):
    os.remove(video_path)
    for frame in glob.glob(f"{frames_folder}/*.jpg"):
        os.remove(frame)
    os.rmdir(frames_folder)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



