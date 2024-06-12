import os
from PIL import Image
directory = 'Original Images'
def convert_bmp_to_png():
    for filename in os.listdir(directory):
        img = Image.open(f'{directory}/{filename}')
        png_filename = f'{directory}/{os.path.splitext(filename)[0]}.png'
        img.save(png_filename)
            
def delete_non_png_files():
    for filename in os.listdir(directory):
        if not filename.endswith(".png"):
            os.remove(f'{directory}/{filename}')
convert_bmp_to_png()
delete_non_png_files()