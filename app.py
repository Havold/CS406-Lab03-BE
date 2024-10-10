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
NOISE_FOLDER = './images/noise'
DENOISE_FOLDER = './images/denoise'
EDGE_FOLDER = './images/edge'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SHARPENED_FOLDER'] = SHARPENED_FOLDER
app.config['NOISE_FOLDER'] = NOISE_FOLDER
app.config['DENOISE_FOLDER'] = DENOISE_FOLDER
app.config['EDGE_FOLDER'] = EDGE_FOLDER

# Tạo thư mục nếu chưa tồn tại
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(SHARPENED_FOLDER):
    os.makedirs(SHARPENED_FOLDER)


# Hàm làm sắc nét ảnh
def sharpening(filepath, sharpen_level=5):
    image = cv2.imread(filepath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    kernel = np.array([[-1,-1,-1], [-1,4+sharpen_level,-1], [-1,-1,-1]])
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
    elif category == 'noise':
        folder_path = app.config['NOISE_FOLDER']
    elif category == 'denoise':
        folder_path = app.config['DENOISE_FOLDER']
    elif category == 'edge':
        folder_path = app.config['EDGE_FOLDER']
    return send_from_directory(folder_path, filename)

@app.route("/edge-detectors", methods=['POST'])
def detect_edge_image():

    def sobel_edge_detect(image, ksize=3):
        ddepth = cv2.CV_16S
        gray_x = cv2.Sobel(src=image, ddepth=ddepth, dx=1, dy=0, ksize=ksize)
        gray_y = cv2.Sobel(src=image, ddepth=ddepth, dx=0, dy=1, ksize=ksize)
        
        abs_gray_x = cv2.convertScaleAbs(gray_x)
        abs_gray_y = cv2.convertScaleAbs(gray_y)
        grad = cv2.addWeighted(abs_gray_x, 0.5, abs_gray_y, 0.5, 0)
        return {
            'gray_x': gray_x,
            'gray_y': gray_y,
            'grad': grad
        }
    
    def prewitt_edge_detect(image):
        kernel_x = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
        kernel_y = np.array([[-1,-1,-1],[0,0,0],[1,1,1]])

        grad_x = cv2.filter2D(image, ddepth=-1, kernel=kernel_x)
        grad_y = cv2.filter2D(image, ddepth=-1, kernel=kernel_y)

        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)

        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

        return {
            'grad_x': grad_x,
            'grad_y': grad_y,
            'grad': grad,
        }        

    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

    method = request.args.get('method').lower()
    low_threshold = int(request.args.get('low'))
    high_threshold = int(request.args.get('high'))
    edge_image = {}

    if method=='sobel':  
        # Sobel Edge
        edge_image = sobel_edge_detect(image)
    elif method=='prewitt':
        # Prewitt Edge
        edge_image = prewitt_edge_detect(image)
    elif method=='canny':
        # Canny Edge
        edge_image = cv2.Canny(image=image, threshold1=low_threshold, threshold2=high_threshold)
    else:
        edge_image['sobel_edge'] = sobel_edge_detect(image)['grad']
        edge_image['prewitt_edge'] = prewitt_edge_detect(image)['grad']
        edge_image['canny_edge'] = cv2.Canny(image=image, threshold1=100, threshold2=200)

    edge_image_urls = {}

    if isinstance(edge_image, dict):
        for name, edge in edge_image.items():
            edge_image_filename = f'{name}_{method}_{filename}'
            edge_image_filepath = os.path.join(app.config['EDGE_FOLDER'], edge_image_filename)
            cv2.imwrite(edge_image_filepath, edge)
            
            edge_image_url = f'/image/edge/{edge_image_filename}'
            edge_image_urls[name] = edge_image_url
    else:
        edge_image_filename = f'{method}_{filename}'
        edge_image_filepath = os.path.join(app.config['EDGE_FOLDER'], edge_image_filename)
        cv2.imwrite(edge_image_filepath, edge_image)
        edge_image_url = f'/image/edge/{edge_image_filename}'
        edge_image_urls['canny_edge_image'] = edge_image_url
    
    return jsonify(edge_image_urls), 200
        
        

    

@app.route("/denoising", methods=['POST'])
def denoising_image():
    def add_sparkle_noise(image, prob, intensity=255):
        output = np.copy(image)
        
        # Tạo một mask có kích thước bằng ảnh đầu vào
        rnd = np.random.rand(image.shape[0], image.shape[1])
        
        # Duyệt qua mask, phần tử nào có value < prob thì sẽ được gán là True
        sparkle_mask = rnd<prob
        output[sparkle_mask] = intensity
        return output
    
    def add_salt_and_pepper_noise(image, prob):
        output = np.copy(image)

        # Tạo một mask có kích thước bằng với ảnh đầu vào 
        rnd = np.random.rand(image.shape[0], image.shape[1])
        
        # Ta sẽ thêm salt noise (255), pepper noise (0) => prob sẽ phải chia đều cho cả 2 => prob/2
        output[rnd < prob/2] = 0
        output[rnd > 1 - prob/2] = 255
        return output
    
    def add_gaussian_noise(image, mean=0, stddev=0.1):
        output = np.copy(image)
        
        # Tạo gaussian noise
        noise = np.random.normal(mean, stddev, image.shape)
        output = output.astype(np.float32)/255.0        
        output = output + noise

        # Giới hạn ngưỡng giá trị từ 0 đến 1 (0 -> 255)
        output = np.clip(output, 0, 1)

        # Chuyển về định dạng uint8
        output = (output*255).astype(np.uint8)

        return output
    
    def mean_filter(image):
        output = np.copy(image)
        kernel = np.ones((6,6))/36
        output = cv2.filter2D(output, ddepth=-1, kernel = kernel)
        return output
    
    def median_filter(image):
        output = np.copy(image)
        output = cv2.medianBlur(output, ksize=5)
        return output

    if 'image' not in request.files:
        return jsonify({'error': 'No file part' }), 400
    
    file = request.files['image']
    if file.filename=='':
        return jsonify({'error': 'No selected file'}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    image = cv2.imread(filepath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    noise_type = request.args.get('type').lower()
    noise_image = None
    
    if (noise_type=='sparkle-noise'):
        # Thêm sparkle noise vào ảnh
        noise_image = add_sparkle_noise(image, prob=0.05)
    elif (noise_type=='salt-pepper-noise'):
        # Thêm salt and pepper noise vào ảnh
        noise_image = add_salt_and_pepper_noise(image, prob=0.05)
    elif (noise_type=='gaussian-noise'):
        # Thêm gaussian noise vào ảnh
        noise_image = add_gaussian_noise(image)

    # Lưu ảnh đã thêm noise    
    # sparkle noise
    noise_filename = f'{noise_type}_noise_{filename}'
    noise_filepath = os.path.join(app.config['NOISE_FOLDER'], noise_filename)
    cv2.imwrite(noise_filepath, cv2.cvtColor(noise_image, cv2.COLOR_BGR2RGB))
    
    # noise image url
    noise_image_url = f'/image/noise/{noise_filename}'

    # DENOISE ẢNH
    # Dùng Mean Filter
    mean_filtered_image = mean_filter(noise_image)
    # Dùng Median Filter
    median_filtered_image = median_filter(noise_image)

    # Lưu ảnh đã được denoise
    # Mean Filter
    mean_filtered_filename = f'mean_filtered_{noise_type}_{filename}'
    mean_filtered_filepath = os.path.join(app.config['DENOISE_FOLDER'], mean_filtered_filename)
    cv2.imwrite(mean_filtered_filepath, cv2.cvtColor(mean_filtered_image, cv2.COLOR_BGR2RGB))

    # Median Filter
    median_filtered_filename = f'median_filtered_{noise_type}_{filename}'
    median_filtered_filepath = os.path.join(app.config['DENOISE_FOLDER'], median_filtered_filename)
    cv2.imwrite(median_filtered_filepath, cv2.cvtColor(median_filtered_image, cv2.COLOR_BGR2RGB))

    # filtered image url
    mean_filtered_image_url = f'/image/denoise/{mean_filtered_filename}'
    median_filtered_image_url = f'/image/denoise/{median_filtered_filename}'
    
    return jsonify({'noise_image_url': noise_image_url,
                    'mean_filtered_image_url': mean_filtered_image_url,
                    'median_filtered_image_url': median_filtered_image_url
                    }), 200

# POST endpoint to handle image upload and find similar images
@app.route('/sharpening', methods=['POST'])
def sharpening_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    sharpen_level = int(request.args.get('level'))

    # Làm sắc nét ảnh
    sharpened_image = sharpening(filepath, sharpen_level)
    
    # Lưu ảnh đã làm sắc nét
    sharpened_filename = f'sharpened_{filename}'
    sharpened_filepath = os.path.join(app.config['SHARPENED_FOLDER'], sharpened_filename)
    cv2.imwrite(sharpened_filepath, cv2.cvtColor(sharpened_image, cv2.COLOR_RGB2BGR))

    # Trả lại URL của ảnh đã làm sắc nét
    sharpened_url = f'/image/sharpened/{sharpened_filename}'
    return jsonify({'sharpened_image_url': sharpened_url}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
