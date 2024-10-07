from flask import Flask, request, jsonify, send_from_directory
import cv2
import os
import numpy as np
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = './images/uploads'
SHARPENED_FOLDER = './images/sharpened'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SHARPENED_FOLDER'] = SHARPENED_FOLDER

# Tạo thư mục nếu chưa tồn tại
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(SHARPENED_FOLDER):
    os.makedirs(SHARPENED_FOLDER)


# Hàm làm sắc nét ảnh
def sharpening(filepath):
    image = cv2.imread(filepath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened_image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)
    return sharpened_image

@app.route('/', methods=['GET'])
def hello():
    return 'Hello'

# Hàm gửi ảnh từ server cho client
@app.route('/image/<category>/<filename>', methods=['GET'])
def get_image(category, filename):
    if category == 'uploads':
        folder_path = app.config['UPLOAD_FOLDER']
    elif category == 'sharpened':
        folder_path = app.config['SHARPENED_FOLDER']
    return send_from_directory(folder_path, filename)


# POST endpoint to handle image upload and find similar images
@app.route('/sharpening', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Làm sắc nét ảnh
    sharpened_image = sharpening(filepath)
    
    # Lưu ảnh đã làm sắc nét
    sharpened_filename = f'sharpened_{filename}'
    sharpened_filepath = os.path.join(app.config['SHARPENED_FOLDER'], sharpened_filename)
    cv2.imwrite(sharpened_filepath, cv2.cvtColor(sharpened_image, cv2.COLOR_RGB2BGR))

    # Trả lại URL của ảnh đã làm sắc nét
    sharpened_url = f'/image/sharpened/{sharpened_filename}'
    return jsonify({'sharpened_image_url': sharpened_url}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
