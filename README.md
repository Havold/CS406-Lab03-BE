# 📷 Image Enhancing, Processing API 

This is a Flask-based application for image processing that provides functionalities like sharpening, noise addition and removal, and edge detection using Sobel, Prewitt, and Canny methods. It also allows users to upload images, apply transformations, and download the processed images.

## 🌟 Features
- **Sharpening**: Adjust the sharpening level of an uploaded image.
- **Noise Addition & Removal**: Add noise (Sparkle, Salt & Pepper, Gaussian) to an image and then apply denoising filters (Mean, Median).
- **Edge Detection**: Detect edges using Sobel, Prewitt, or Canny methods.

## 🛠️ Requirements

Before running the project, make sure you have the following installed:
- Python 3.x, 3.12.6 __(Recommend)__
- Flask 3.0.3
- OpenCV 4.10.0
- NumPy 2.1.1
- SciPy 1.14.1
- Flask-CORS 5.0.0

You can install all dependencies by running:

```
pip install -r requirements.txt
```

## 🚀 Getting Started
1. Clone the repository:
```
git clone https://github.com/Havold/CS406-Lab03-BE.git
cd CS406-Lab03-BE
```
2. Create necessary directories:

Make sure the following directories exist for image uploads and processing:
- `./images/uploads/`
- `./images/sharpened/`
- `./images/noise/`
- `./images/denoise/`
- `./images/edge/`
3. Install dependencies
Install the required Python packages using:
```
pip install -r requirements.txt
```
4. Run the Flask server:
```
python app.py
```
5. The server will start at http://localhost:5000.

## ❗ API Endpoints
1. Sharpen Image
   - **URL**: `/sharpening`
   - **Method**: `POST`
   - **Parameters**:
      - `level`: Sharpening intensity (integer).
   - **File**: Image file (JPEG/PNG).
   - **Response**: Returns the URL of the sharpened image.
2. Edge Detection
   - **URL**: `/edge-detectors`
   - **Method**: `POST`
   - **Parameters**:
      - `method`: `sobel`, `prewitt`, or `canny`.
      - `low`: Lower threshold (for Canny).
      - `high`: Upper threshold (for Canny).
   - **File**: Image file (JPEG/PNG).
   - **Response**: Returns URLs of the edge-detected images.
3. Noise Addition and Denoising
   - **URL**: `/denoising`
   - **Method**: `POST`
   - **Parameters**:
      - `type`: `sparkle-noise`, `salt-pepper-noise`, or `gaussian-noise`.
   - **File**: Image file (JPEG/PNG).
   - **Response**: Returns URLs of the noisy and denoised images.
4. Get Processed Image
   - **URL**: `/image/<category>/<filename>`
   - **Method**: `GET`
   - **Parameters**:
      - `category`: `uploads`, `sharpened`, `noise`, `denoise`, or `edge`.
      - `filename`: Name of the image file.
   - **Response**: Returns the processed image.

## 🔥 Usage
Once the server is running, you can test the application by sending requests via a tool like `Postman` or via a frontend application to interact with the API.

---------------------------------------------------------
# 📷 API xử lý, cải thiện hình ảnh.

Đây là một API dựa trên Flask để xử lý ảnh, cung cấp các tính năng như làm sắc nét, thêm và loại bỏ nhiễu, phát hiện biên cạnh bằng các phương pháp Sobel, Prewitt, và Canny. Ứng dụng cho phép người dùng tải ảnh lên, áp dụng các thao tác xử lý, và tải về các ảnh đã qua xử lý.

## 🌟 Tính năng
- **Làm sắc nét**: Điều chỉnh mức độ làm sắc nét cho ảnh tải lên.
- **Thêm và Loại bỏ Nhiễu**: Thêm nhiễu (Sparkle, Salt & Pepper, Gaussian) vào ảnh và sau đó áp dụng các bộ lọc khử nhiễu (Mean, Median).
- **Phát hiện biên cạnh**: Phát hiện biên cạnh bằng phương pháp Sobel, Prewitt, hoặc Canny.

## 🛠️ Requirements

Trước khi chạy dự án, hãy đảm bảo bạn đã cài đặt các dependencies sau:
- Python 3.x, 3.12.6 __(Đề xuất)__
- Flask 3.0.3
- OpenCV 4.10.0
- NumPy 2.1.1
- SciPy 1.14.1
- Flask-CORS 5.0.0

Bạn có thể cài đặt tất cả các thư viện trên bằng cách chạy:

```
pip install -r requirements.txt
```

## 🚀 Bắt đầu thôi!
1. Clone dự án về
```
git clone https://github.com/Havold/CS406-Lab03-BE.git
cd CS406-Lab03-BE
```
2. Tạo các thư mục cần thiết

Đảm bảo các thư mục sau đây tồn tại để lưu trữ ảnh tải lên và xử lý:
- `./images/uploads/`
- `./images/sharpened/`
- `./images/noise/`
- `./images/denoise/`
- `./images/edge/`
2. Cài đặt các dependencies:
```
pip install -r requirements.txt
```
4. Chạy Flask server:
```
python app.py
```
5. Server sẽ chạy ở: http://localhost:5000.

## ❗ API Endpoints
1. Làm sắc nét ảnh
   - **URL**: `/sharpening`
   - **Method**: `POST`
   - **Parameters**:
      - `level`: Mức độ làm sắc nét (số nguyên).
   - **File**: Tệp ảnh (JPEG/PNG).
   - **Response**: Trả về URL của ảnh đã làm sắc nét.
2. Phát hiện biên cạnh
   - **URL**: `/edge-detectors`
   - **Method**: `POST`
   - **Parameters**:
      - `method`: `sobel`, `prewitt`, hoặc `canny`.
      - `low`: Lower threshold (cho Canny).
      - `high`: Upper threshold (cho Canny).
   - **File**: Tệp ảnh (JPEG/PNG).
   - **Response**: Trả về URL các ảnh đã được phát hiện biên cạnh.
3. Thêm và loại bỏ nhiễu
   - **URL**: `/denoising`
   - **Method**: `POST`
   - **Parameters**:
      - `type`: `sparkle-noise`, `salt-pepper-noise`, hoặc `gaussian-noise`.
   - **File**: Tệp ảnh (JPEG/PNG).
   - **Response**: Trả về URL của các ảnh đã thêm nhiễu và khử nhiễu
4. Lấy ảnh đã xử lý
   - **URL**: `/image/<category>/<filename>`
   - **Method**: `GET`
   - **Parameters**:
      - `category`: `uploads`, `sharpened`, `noise`, `denoise`, hoặc `edge`.
      - `filename`: Tên tệp ảnh.
   - **Response**: Trả về ảnh đã xử lý

## 🔥 Sử dụng
Khi server đã chạy, bạn có thể kiểm tra ứng dụng bằng cách gửi các yêu cầu qua các công cụ như `Postman` hoặc thông qua một ứng dụng frontend để tương tác với API.
