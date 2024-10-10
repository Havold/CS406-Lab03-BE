# 🌟 Image Enhancing API 

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
- ./images/uploads/
- ./images/sharpened/
- ./images/noise/
- ./images/denoise/
- ./images/edge/
3. Install dependencies:
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
      - `low`: Lower threshold (for Canny).
      - `high`: Upper threshold (for Canny).
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
Once the server is running, you can test the application by sending requests via a tool like Postman or via a frontend application to interact with the API.

---------------------------------------------------------
# :sunglasses: API Tính khoảng cách và tìm các ảnh tương đồng thông qua histogram

API dựa trên Flask này cho phép người dùng tải lên hình ảnh và so sánh biểu đồ histogram của hình ảnh đó với cơ sở dữ liệu hình ảnh được lưu trữ để tìm ra hình ảnh giống nhau nhất. API hỗ trợ cả biểu đồ histogram cân bằng và không cân bằng.

## 🌟 Tính năng
- Tải lên một hình ảnh và tính toán histogram của nó.
- So sánh histogram của hình ảnh được tải lên với hình ảnh đã lưu trữ.
- Lấy N hình ảnh giống nhau nhất dựa trên khoảng cách Euclid.
- Tùy chọn sử dụng equalized histogram để so sánh tốt hơn.

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
git clone https://github.com/Havold/CS406-Lab02-BE-Raw.git
cd CS406-Lab02-BE-Raw
```
2. Cài đặt các dependencies:
```
pip install -r requirements.txt
```
3. Thiết lập cấu trúc thư mục:
   - Tải xuống dataset và tạo một thư mục __images__ trong thư mục gốc và đặt dataset vừa tải về vào thư mục __images__ vừa tạo (nhớ giải nén).
   - Cấu trúc thư mục sẽ như sau: __CS406-Lab02-BE-Raw/images/seg__, __CS406-Lab02-BE-Raw/images/seg_test__ (__seg_test__ có thể cần phải đưa vào vì chúng ta sẽ chỉ truy vấn trong thư mục seg).
   - Link dataset: https://drive.google.com/file/d/1F6sPtl0H-Sh7XPrAojDKcz_rBoUl_fgu/view?usp=sharing
![directory](./directory.jpg)
4. Chạy Flask server:
```
python app.py
```
5. Server sẽ chạy ở: http://localhost:5000.

## ⚠️ Lưu ý quan trọng
- Hai file __histograms_equalized.json__ và __histograms.json__ được tạo từ __create-json-file.ipynb__.
- Bạn có thể tải xuống và chạy __create-json-file.ipynb__ tại đây: https://drive.google.com/file/d/15uB2WsK3YFxfee1_cC2OmF5BN7rF4-iM/view?usp=sharing
