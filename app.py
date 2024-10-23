# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import cv2
# import glob
# from deepface import DeepFace
# from werkzeug.utils import secure_filename
# import numpy as np
# from subprocess import run


# app = Flask(__name__)
# application = app
# CORS(app)  # Enables CORS for all routes

# # Create upload and frames directory
# UPLOAD_FOLDER = 'uploads'
# FRAMES_FOLDER = 'frames'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Ensure directories exist
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(FRAMES_FOLDER, exist_ok=True)


# @app.route('/analyze-video', methods=['POST'])
# def analyze_video():
#     if 'file' not in request.files:
#         return jsonify({
#             "status": "error",
#             "message": "No file provided",
#             "data": None
#         }), 400

#     video_file = request.files['file']
#     video_filename = secure_filename(video_file.filename)
#     video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
#     video_file.save(video_path)

#     try:
#         # Step 1: Extract frames from the video
#         frames_folder = extract_frames(video_path)

#         # Step 2: Analyze the frames for emotions
#         emotion_data = analyze_emotions(frames_folder)

#         # Step 3: Aggregate emotion results
#         averaged_emotions = aggregate_emotions(emotion_data)

#         # Clean up files after processing
#         clean_up(video_path, frames_folder)

#         # Return the response in the desired format
#         return jsonify({
#             "status": "success",
#             "message": "Video analysis completed successfully",
#             "data": {
#                 "averaged_emotions": averaged_emotions
#             }
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": f"An error occurred during video analysis: {str(e)}",
#             "data": None
#         }), 500



# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "API works"})


# def extract_frames(video_path):
#     frames_folder = os.path.join(FRAMES_FOLDER, os.path.basename(video_path).split('.')[0])
#     os.makedirs(frames_folder, exist_ok=True)

#     # Extract 1 frame per second using ffmpeg
#     command = f"ffmpeg -i {video_path} -vf format=yuv420p,fps=1 {frames_folder}/frame_%04d.jpg"
#     # command = f"ffmpeg -i {video_path} -vf fps=1 {frames_folder}/frame_%04d.jpg"
#     # run(command, shell=True)
#     result = run(command, shell=True, capture_output=True, text=True)
#     print(result.stdout)
#     print(result.stderr)
    
#     return frames_folder

# def analyze_emotions(frames_folder):
#     results = []

#     for frame_path in glob.glob(f"{frames_folder}/*.jpg"):
#         try:
#             # Analyze the frame using DeepFace's emotion model
#             analysis = DeepFace.analyze(img_path=frame_path, actions=['emotion'])

#             # Ensure analysis is a list and access the first element
#             if isinstance(analysis, list) and len(analysis) > 0:
#                 emotions = analysis[0]['emotion']  # Access the 'emotion' data from the first dictionary
#                 results.append({
#                     "frame": frame_path,
#                     "emotions": emotions
#                 })
#             else:
#                 print(f"Unexpected analysis structure for {frame_path}: {analysis}")

#         except Exception as e:
#             print(f"Error analyzing {frame_path}: {e}")

#     return results


# def aggregate_emotions(emotion_data):
#     # If no frames were processed, return an empty result
#     if not emotion_data:
#         return {}

#     emotion_keys = emotion_data[0]['emotions'].keys()
#     aggregated_emotions = {key: [] for key in emotion_keys}

#     # Aggregate emotion scores for each frame
#     for data in emotion_data:
#         for emotion, score in data['emotions'].items():
#             aggregated_emotions[emotion].append(score)

#     # Calculate the average for each emotion
#     averaged_emotions = {emotion: np.mean(scores) for emotion, scores in aggregated_emotions.items()}

#     return averaged_emotions

# def clean_up(video_path, frames_folder):
#     os.remove(video_path)
#     for frame in glob.glob(f"{frames_folder}/*.jpg"):
#         os.remove(frame)
#     os.rmdir(frames_folder)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)



# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import cv2
# import glob
# from deepface import DeepFace
# from werkzeug.utils import secure_filename
# import numpy as np
# from subprocess import run
# import concurrent.futures


# app = Flask(__name__)
# application = app
# CORS(app)  # Enables CORS for all routes

# # Create upload and frames directory
# UPLOAD_FOLDER = 'uploads'
# FRAMES_FOLDER = 'frames'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Ensure directories exist
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(FRAMES_FOLDER, exist_ok=True)


# @app.route('/analyze-video', methods=['POST'])
# def analyze_video():
#     if 'file' not in request.files:
#         return jsonify({
#             "status": "error",
#             "message": "No file provided",
#             "data": None
#         }), 400

#     video_file = request.files['file']
#     video_filename = secure_filename(video_file.filename)
#     video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
#     video_file.save(video_path)

#     try:
#         # Step 1: Extract frames from the video
#         frames_folder = extract_frames(video_path)

#         # Step 2: Analyze the frames for emotions
#         emotion_data = analyze_emotions(frames_folder)

#         # Step 3: Aggregate emotion results
#         averaged_emotions = aggregate_emotions(emotion_data)

#         # Clean up files after processing
#         clean_up(video_path, frames_folder)

#         # Return the response in the desired format
#         return jsonify({
#             "status": "success",
#             "message": "Video analysis completed successfully",
#             "data": {
#                 "averaged_emotions": averaged_emotions
#             }
#         }), 200

#     except Exception as e:
#         return jsonify({
#             "status": "error",
#             "message": f"An error occurred during video analysis: {str(e)}",
#             "data": None
#         }), 500



# @app.route('/', methods=['GET'])
# def home():
#     return jsonify({"message": "API works"})


# def extract_frames(video_path):
#     frames_folder = os.path.join(FRAMES_FOLDER, os.path.basename(video_path).split('.')[0])
#     os.makedirs(frames_folder, exist_ok=True)

#     # Extract fewer frames for faster processing
#     command = f"ffmpeg -i {video_path} -vf format=yuv420p,fps=0.5 {frames_folder}/frame_%04d.jpg"
#     result = run(command, shell=True, capture_output=True, text=True)
#     print(result.stdout)
#     print(result.stderr)
    
#     return frames_folder

# def analyze_emotions(frames_folder):
#     frame_paths = glob.glob(f"{frames_folder}/*.jpg")

#     def analyze_frame(frame_path):
#         try:
#             analysis = DeepFace.analyze(img_path=frame_path, actions=['emotion'])
#             if isinstance(analysis, list) and len(analysis) > 0:
#                 emotions = analysis[0]['emotion']
#                 return {"frame": frame_path, "emotions": emotions}
#         except Exception as e:
#             print(f"Error analyzing {frame_path}: {e}")
#         return None

#     # Use a ThreadPoolExecutor for parallel analysis of frames
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         results = list(executor.map(analyze_frame, frame_paths))

#     # Filter out any None results due to errors
#     return [result for result in results if result is not None]


# def aggregate_emotions(emotion_data):
#     # If no frames were processed, return an empty result
#     if not emotion_data:
#         return {}

#     emotion_keys = emotion_data[0]['emotions'].keys()
#     aggregated_emotions = {key: [] for key in emotion_keys}

#     # Aggregate emotion scores for each frame
#     for data in emotion_data:
#         for emotion, score in data['emotions'].items():
#             aggregated_emotions[emotion].append(score)

#     # Calculate the average for each emotion
#     averaged_emotions = {emotion: np.mean(scores) for emotion, scores in aggregated_emotions.items()}

#     return averaged_emotions

# def clean_up(video_path, frames_folder):
#     os.remove(video_path)
#     for frame in glob.glob(f"{frames_folder}/*.jpg"):
#         os.remove(frame)
#     os.rmdir(frames_folder)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import cv2
import glob
from deepface import DeepFace
from werkzeug.utils import secure_filename
import numpy as np
from subprocess import run
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time


app = Flask(__name__)
application = app
CORS(app)  # Enables CORS for all routes

# Create upload and frames directory
UPLOAD_FOLDER = 'uploads'
FRAMES_FOLDER = 'frames'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FRAMES_FOLDER, exist_ok=True)


@app.route('/analyze-video', methods=['POST'])
def analyze_video():
    start = time()
    if 'file' not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file provided",
            "data": None
        }), 400

    video_file = request.files['file']
    if not video_file.filename:
        return jsonify({
            "status": "error",
            "message": "No file selected",
            "data": None
        }), 400

    # Add file size limit
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    if request.content_length > MAX_FILE_SIZE:
        return jsonify({
            "status": "error",
            "message": "File size exceeds limit (50MB)",
            "data": None
        }), 413

    video_filename = secure_filename(video_file.filename)
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
    
    try:
        video_file.save(video_path)
        frames_folder = extract_frames(video_path)
        emotion_data = analyze_emotions(frames_folder)
        averaged_emotions = aggregate_emotions(emotion_data)
        
        # Clean up as soon as possible
        clean_up(video_path, frames_folder)
        
        return jsonify({
            "status": "success",
            "message": "Video analysis completed",
            "data": {"averaged_emotions": averaged_emotions}
        }), 200
        print(f"Total processing time: {time() - start:.2f} seconds")

    except Exception as e:
        # Ensure cleanup happens even if processing fails
        if os.path.exists(video_path):
            os.remove(video_path)
        return jsonify({
            "status": "error",
            "message": str(e),
            "data": None
        }), 500


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "API works"})


def extract_frames(video_path):
    frames_folder = os.path.join(FRAMES_FOLDER, os.path.basename(video_path).split('.')[0])
    os.makedirs(frames_folder, exist_ok=True)

    # Optimize ffmpeg command:
    # - Add scale parameter to resize frames
    # - Use select filter to reduce number of frames
    command = (
        f"ffmpeg -i {video_path} "
        f"-vf \"scale=240:-1,select='not(mod(n,15))'\" " # Process every 15th frame and resize
        f"-vsync vfr "  # Variable frame rate for better performance
        f"{frames_folder}/frame_%04d.jpg"
    )
    
    result = run(command, shell=True, capture_output=True, text=True)
    return frames_folder

def analyze_single_frame(frame_path):
    try:
        analysis = DeepFace.analyze(img_path=frame_path, actions=['emotion'])
        if isinstance(analysis, list) and len(analysis) > 0:
            return {
                "frame": frame_path,
                "emotions": analysis[0]['emotion']
            }
    except Exception as e:
        print(f"Error analyzing {frame_path}: {e}")
        return None

def analyze_emotions(frames_folder):
    frames = glob.glob(f"{frames_folder}/*.jpg")
    results = []
    
    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_frame = {executor.submit(analyze_single_frame, frame): frame 
                          for frame in frames}
        
        for future in as_completed(future_to_frame):
            result = future.result()
            if result:
                results.append(result)
    
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
    try:
        # Remove video file immediately after frame extraction
        os.remove(video_path)
        
        # Use a generator for memory-efficient file deletion
        for frame in (f for f in os.listdir(frames_folder) if f.endswith('.jpg')):
            os.remove(os.path.join(frames_folder, frame))
            
        os.rmdir(frames_folder)
    except Exception as e:
        print(f"Error during cleanup: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)







