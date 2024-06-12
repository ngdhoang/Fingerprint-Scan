import cv2
import os
from PIL import Image
# Đường dẫn đến thư mục chứa ảnh
folder_path = 'Original Images'
# Đường dẫn đến thư mục lưu ảnh nhị phân
output_folder_path = 'Changes Images'

# Tạo thư mục lưu ảnh nhị phân nếu chưa tồn tại
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)
def binarize_image_gray(image_path):
    # Đọc ảnh xám
    gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Làm mịn ảnh với bộ lọc Gaussian
    blurred_image = cv2.GaussianBlur(gray_image, (1, 1), 0)  # Thay đổi kích thước kernel ở đây

    # Chuyển ảnh sang ảnh nhị phân với ngưỡng cố định
    _, binary_image = cv2.threshold(blurred_image, 150, 255, cv2.THRESH_BINARY)

    return binary_image

# Lặp qua tất cả các tệp trong thư mục ảnh
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Đường dẫn đến tệp ảnh
        image_path = os.path.join(folder_path, filename)
        
        # Nhị phân hóa ảnh
        binary_image = binarize_image_gray(image_path)
        
        # Lưu ảnh nhị phân vào thư mục đầu ra
        output_path = os.path.join(output_folder_path, filename)
        cv2.imwrite(output_path, binary_image)

print("Hoàn thành quá trình nhị phân hóa ảnh.")

