from PIL import Image
import os

def crop_images(image_path, status):
    directory = 'Changes Images'
    left_image = Image.open(image_path)
    left_width, left_height = left_image.size

    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            img = Image.open(f'{directory}/{filename}')
            w, h = img.size
            if status == 0:
                cropped_img = img.crop((left_width, 0, w - left_width, h))
            elif status == 1:
                cropped_img = img.crop((0, 0, w - left_width, h))
            elif status == 2:
                cropped_img = img.crop((0, left_height, w, h - left_height))
            else:
                cropped_img = img.crop((0, 0, w, h - left_height))
            cropped_filename = f'{directory}/{filename}'
            cropped_img.save(cropped_filename)
crop_images('Bounds Image/left.png', 0)
crop_images('Bounds Image/right.png', 1)
crop_images('Bounds Image/bottom.png', 3)
crop_images('Bounds Image/top.png', 2)
print("Hoàn thành quá trình cắt ảnh.")

