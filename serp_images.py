import requests
import os
import json
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()


# Your SERP API Key loaded from .env file

API_KEY = os.getenv("SERP_API_KEY")

# Perform Google Image Search: Use the SERP API to perform a Google Image search.

def google_img_search(query):
    params = {
        "q": query,
        "tbm": "isch",
        "ijn": 0,
        "api_key": API_KEY,
    }

    response = requests.get("https://serpapi.com/search", params=params)

    return response.json()


# Extract Image URLs: The JSON response from the SERP API includes URLs to the images. You can extract these URLs.

def extract_img_urls(response_json):
    image_results = response_json['images_results']
    img_urls = []
    for result in image_results:
        print(result)  # print to inspect the actual data
        if 'original' in result:
            img_urls.append(result['original'])
    return img_urls


# Download Images: Use the extracted URLs to download the images and save to the local directory.

def download_images(img_urls, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    for i, img_url in enumerate(img_urls):
        response = requests.get(img_url)

        with open(os.path.join(save_dir, f"{i}.png"), "wb") as f:
            f.write(response.content)


# Run the Process: Combine these functions to perform the image search and download the images.

def main(query):
    response_json = google_img_search(query)
    img_urls = extract_img_urls(response_json)
    return img_urls


if __name__ == "__main__":
    main()
