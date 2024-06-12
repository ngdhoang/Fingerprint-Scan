from PIL import Image
import os
import numpy as np
import pandas as pd

def calculate_clockwise_differences(grid):
    # Define the order of pixels in clockwise direction
    clockwise_order = [grid[0, 0], grid[0, 1], grid[0, 2], grid[1, 2], grid[2, 2], grid[2, 1], grid[2, 0], grid[1, 0]]
    differences = [abs(clockwise_order[i] - clockwise_order[i-1]) for i in range(len(clockwise_order))]
    total_difference = sum(differences)
    return total_difference / 2

def feature_extraction(cropped_img):
    img_array = np.array(cropped_img)
    start_points = 0
    connection_points = 0
    branch_points = 0
    # Pad the image array with a border of zeros
    img_array = np.pad(img_array, pad_width=1, mode='constant', constant_values=0)
    for i in range(1, img_array.shape[0] - 1):
        for j in range(1, img_array.shape[1] - 1):
            # Only consider non-zero pixels
            if img_array[i, j] != 0:
                # Get 3x3 grid around pixel
                grid = img_array[i-1:i+2, j-1:j+2]
                # Normalize grid to 0 and 1
                grid = np.where(grid != 0, 1, 0)
                total_difference = calculate_clockwise_differences(grid)
                if total_difference <= 1:
                    start_points += 1
                elif total_difference == 2:
                    connection_points += 1
                elif total_difference > 2:
                    branch_points += 1
    return [start_points, connection_points, branch_points]

def save_to_csv(data, img_name, n):
    df = pd.DataFrame([data], columns=['start_points', 'connection_points', 'branch_points'])
    df.insert(0, 'filename', img_name)
    if not os.path.isfile('Data/fingerprint_characteristic_data_' + f"{n}x{n}.csv"):
        df.to_csv('Data/fingerprint_characteristic_data_' + f"{n}x{n}.csv", mode='w', header=True, index=False)
    else:
        df.to_csv('Data/fingerprint_characteristic_data_' + f"{n}x{n}.csv", mode='a', header=False, index=False)

def crop_images(img, img_name, n, hasInput=False):
    w, h = img.size
    w_step = w // n
    h_step = h // n
    feature_result = []
    for i in range(n):
        for j in range(n):
            left = i * w_step
            upper = j * h_step
            right = (i + 1) * w_step
            lower = (j + 1) * h_step
            cropped_img = img.crop((left, upper, right, lower))
            if hasInput:
                feature_result.append(feature_extraction(cropped_img))
            else:
                save_to_csv(feature_extraction(cropped_img), img_name, n)
    return feature_result

def read_data(n):
    directory = 'Changes Images'
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            img = Image.open(f'{directory}/{filename}')
            crop_images(img, filename, n)
# for i in range(1, 16):            
#     read_data(i)

