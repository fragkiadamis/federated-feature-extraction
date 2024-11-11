import os
import sys

import numpy as np
import SimpleITK as sitk
import requests


# Function to extract features from an image
def extract_features(data_path):
    features = []
    for sample in os.listdir(data_path):
        print(f"Extracting from image {sample}")

        sample_id = sample.split("_")[2]
        image_path = os.path.join(data_path, sample)
        image = sitk.ReadImage(str(image_path))
        image_array = sitk.GetArrayFromImage(image)

        features.append({sample_id: {
            'min_intensity': float(np.min(image_array)),
            'max_intensity': float(np.max(image_array)),
            'mean_intensity': float(np.mean(image_array)),
            'std_intensity': float(np.std(image_array)),
            'histogram_bins': [float(x) for x in np.histogram(image_array, bins=10)[0]]
        }})

    return features

# Send extracted features to the server
def send_features_to_server(client_id, features, server_url="http://127.0.0.1:5000/upload"):
    payload = {"client_id": client_id, "features": features}
    response = requests.post(server_url, json=payload)
    return response.status_code, response.json()

def main():
    client_id, data_path = sys.argv[1], sys.argv[2]
    features = extract_features(data_path)
    status_code, response = send_features_to_server(client_id, features)
    print("Response from server:", response, status_code)

if __name__ == "__main__":
    main()
