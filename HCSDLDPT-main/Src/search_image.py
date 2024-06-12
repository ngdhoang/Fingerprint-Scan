import pandas as pd
import heapq
import math
import numpy as np

data_dict = {}

def calculate_average_distance(distances):
    if not distances:  
        return 0
    Q1 = np.percentile(distances, 25)
    Q3 = np.percentile(distances, 75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    filtered_distances = [d for d in distances if lower_bound <= d <= upper_bound]

    if not filtered_distances: 
        return 0
    return sum(filtered_distances) / len(filtered_distances)

def calculate_similarity(feature_current, feature_data):
    distances = []
    for i in range(len(feature_data)):
        distance = math.sqrt(sum((x - y) ** 2 for x, y in zip(feature_current[i], feature_data[i])))
        distances.append(distance)
    return calculate_average_distance(distances)

def read_data(n):
    data_dict.clear()
    df = pd.read_csv('Data/fingerprint_characteristic_data_' + f"{n}x{n}.csv")
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # If the filename is not already a key in the dictionary, add it with an empty list as its value
        if row['filename'] not in data_dict:
            data_dict[row['filename']] = []
        # Append the values as a list to the filename key in the dictionary
        data_dict[row['filename']].append([row['start_points'], row['connection_points'], row['branch_points']])

def search_image(feature_current, n):
    if (not data_dict):
        read_data(n)
    # Create a min-heap to store the top three smallest scores
    result = []
    # Iterate over each key-value pair in the data dictionary
    for key, value in data_dict.items():
        similarity_score = calculate_similarity(feature_current, value)
        # Push the tuple (similarity_score, key) into the heap
        if len(result) < 3:
            heapq.heappush(result, (-similarity_score, key))
        else:
            heapq.heappushpop(result, (-similarity_score, key))
    
    # Convert the heap into a sorted list to return the keys
    result.sort(reverse=True)
    return result

