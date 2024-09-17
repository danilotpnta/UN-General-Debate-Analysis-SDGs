import requests
import os
from tqdm import tqdm

# Function to download a file with progress tracking using tqdm
def download_file(file_url, output_dir, file_name):
    # Stream the file and get the total file size from headers
    response = requests.get(file_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    file_path = os.path.join(output_dir, file_name)
    
    # Download the file in chunks and display progress using tqdm
    with open(file_path, 'wb') as file, tqdm(
        desc=file_name,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))

# Main function to fetch dataset metadata and download all files
def download_dataset(dataset_doi="10.7910/DVN/0TJX8Y", dataverse_server="dataverse.harvard.edu", output_dir="data/raw"):

    print("Downloading dataset...")

    # API endpoint to retrieve dataset information
    dataset_url = f"https://{dataverse_server}/api/datasets/:persistentId/?persistentId=doi:{dataset_doi}"
    
    # Fetch dataset metadata
    response = requests.get(dataset_url)
    if response.status_code == 200:
        dataset_metadata = response.json()
        
        # Directory to save files
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Extract file information from the metadata
        files = dataset_metadata['data']['latestVersion']['files']
        
        for file in files:
            file_info = file['dataFile']
            file_name = file_info['filename']
            file_id = file_info['id']
            
            # Construct the file download URL
            file_download_url = f"https://{dataverse_server}/api/access/datafile/{file_id}"
            
            # Full path of the file to check if it already exists
            file_path = os.path.join(output_dir, file_name)
            
            # Check if the file already exists
            if os.path.exists(file_path):
                print(f"File already downloaded: {file_name}")
            else:
                # Download the file with progress bar
                download_file(file_download_url, output_dir, file_name)
    else:
        print(f"Failed to fetch dataset metadata: {response.status_code}")