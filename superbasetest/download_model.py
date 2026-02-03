import os
import requests
import sys

# Standard path for rembg u2net model on Windows
home_dir = os.path.expanduser("~")
u2net_dir = os.path.join(home_dir, ".u2net")
model_path = os.path.join(u2net_dir, "u2net.onnx")
model_url = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"

def download_model():
    print(f"Creating directory: {u2net_dir}")
    os.makedirs(u2net_dir, exist_ok=True)
    
    print(f"Downloading u2net model from {model_url}...")
    print("This might take a while depending on your internet connection.")
    
    try:
        response = requests.get(model_url, stream=True, timeout=120) # 2 minute timeout
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024 # 1 Kibibyte
        
        with open(model_path, 'wb') as file:
            downloaded = 0
            for data in response.iter_content(block_size):
                file.write(data)
                downloaded += len(data)
                # Simple progress indicator
                if total_size > 0:
                    percent = int(100 * downloaded / total_size)
                    if percent % 10 == 0:
                        print(f"Progress: {percent}%", end='\r')
                        
        print(f"\nModel downloaded successfully to {model_path}")
        
    except Exception as e:
        print(f"\nError downloading model: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if os.path.exists(model_path):
        print(f"Model already exists at {model_path}")
        # Optional: check size or overwrite? For now assume if it exists it's fine, 
        # but the user had a timeout so maybe it's partial or missing.
        # If it's 0 bytes, we should redownload.
        if os.path.getsize(model_path) == 0:
            print("File is empty, redownloading...")
            download_model()
        else:
            print("Skipping download.")
    else:
        download_model()
