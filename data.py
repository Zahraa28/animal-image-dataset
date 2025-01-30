import requests
import os
from io import BytesIO
from PIL import Image
from tqdm import tqdm


# Unsplash API endpoint
API_url = "https://api.unsplash.com/search/photos"

# Unsplash API credentials
ACCESS_KEY = "jiu_9eGLP6EtDRK5WJBF6oIKM4aNENRi-hUakOfeTqc"
PER_PAGE = 30
TOTAL_PAGES = 50  # Total API requests/pages to fetch

# Search query and directory to save images
SEARCH_QUERY = "dolphin"
data_dir = "animals"
image_dir = os.path.join(data_dir, SEARCH_QUERY)

def download_images():
    total_download = 0
    page = 1

    while page <= TOTAL_PAGES:
        print(f"Fetching page {page}...")
        # Request parameters
        params = {
            "query" : SEARCH_QUERY,
            "page" : page ,
            "per_page" : PER_PAGE,
            "client_id" :ACCESS_KEY
        }
        # Make the API request
        try:
            response = requests.get(API_url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch data from API: {e}")
            break
        
        # Parse JSON response
        src = response.json()
        images = src.get("results",[])
        print(f"Found {len(images)}, images on page {page}.")
        
        for img in tqdm(images, desc=f"Downloading images (page {page})"):
            
            # Get the URL of the image
            img_url = img["urls"]["full"]
            try:
                # Download the image
                img_data = requests.get(img_url)
                img_data.raise_for_status()
                
                # Save the image
                img_content = Image.open(BytesIO(img_data.content))
                img_path = os.path.join(image_dir, f"image_{total_download+1}.jpg")
                img_content.save(img_path)
                
                total_download += 1

            except Exception as e :
                print(f"failed to save {total_download+1}:{e}")
        # Increment the page
        page += 1
    print(f"Downloaded {total_download} images to {image_dir}.")

# Run the script
download_images()

