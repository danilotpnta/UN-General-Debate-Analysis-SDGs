import requests
import os
import tarfile
import shutil  
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

# Function to remove files starting with `._` after uncompressing
def remove_resource_files(output_dir):
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.startswith("._"):
                file_path = os.path.join(root, file)
                os.remove(file_path)


# Function to rename directories
def rename_directory(old_name, new_name):
    old_path = os.path.join(old_name)
    new_path = os.path.join(new_name)
    if os.path.exists(old_path):
        shutil.move(old_path, new_path)

# Function to uncompress .tgz files
def uncompress_tgz(file_path, output_dir):
    try:
        with tarfile.open(file_path, "r:gz") as tar:
            tar.extractall(path=output_dir)
        print(f"Uncompressed: {file_path}")
        
        # Remove resource files (`._` files)
        remove_resource_files(output_dir)
        
        # Rename the TXT directory to UNGDC_
        rename_directory(os.path.join(output_dir, "TXT"), os.path.join(output_dir, "UNGDC_1946-2023"))
    except Exception as e:
        print(f"Failed to uncompress {file_path}: {e}")

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
        
        # Step 1: Download all files
        files_to_uncompress = []
        files = dataset_metadata['data']['latestVersion']['files']
        
        for file in files:
            file_info = file['dataFile']
            file_name = file_info['filename']
            file_id = file_info['id']
            
            # Construct the file download URL
            file_download_url = f"https://{dataverse_server}/api/access/datafile/{file_id}"
            
            # Full path of the file to check if it already exists
            file_path = os.path.join(output_dir, file_name)
            
            # Check if the file is already downloaded
            if os.path.exists(file_path):
                print(f"File already downloaded: {file_name}")
            else:
                # Download the file if not already downloaded
                download_file(file_download_url, output_dir, file_name)
            
            # Collect .tgz files for uncompression
            if file_name.endswith(".tgz"):
                files_to_uncompress.append(file_path)

        # Step 2: Uncompress the downloaded .tgz files
        print("Uncompressing data...")
        for file_path in files_to_uncompress:
            uncompressed_dir = file_path.replace('.tgz', '')  # Folder where the uncompressed data will go
            if not os.path.exists(uncompressed_dir):
                uncompress_tgz(file_path, output_dir)
            else:
                print(f"Data already uncompressed: {uncompressed_dir}")
    else:
        print(f"Failed to fetch dataset metadata: {response.status_code}")

if __name__ == "__main__":
    download_dataset()