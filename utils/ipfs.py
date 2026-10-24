import requests
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Kaleido IPFS API endpoint
KALEIDO_IPFS_URL = os.getenv("KALEIDO_IPFS_URL", "")

# App ID and Password for Kaleido's IPFS service
KALEIDO_APP_ID = os.getenv("KALEIDO_APP_ID", "")
KALEIDO_APP_PASSWORD = os.getenv("KALEIDO_APP_PASSWORD", "")

def upload_to_ipfs(file_path):
    if not (KALEIDO_IPFS_URL and KALEIDO_APP_ID and KALEIDO_APP_PASSWORD):
        logger.warning("Kaleido IPFS credentials not configured in environment. Skipping upload.")
        return None

    try:
        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            # Set up authentication using Kaleido App ID and Password
            auth = (KALEIDO_APP_ID, KALEIDO_APP_PASSWORD)

            # Upload the file to Kaleido's IPFS service with the form entry 'path'
            response = requests.post(
                KALEIDO_IPFS_URL,
                files={'path': file},  # Kaleido requires the form entry to be named 'path'
                auth=auth  # Add authentication
            )

            # Check if the request was successful
            if response.status_code == 200:
                print(f"Full response JSON: {response.json()}")
                response_json = response.json()
                if 'Hash' in response_json:
                    return response_json['Hash']
                else:
                    print("Hash not found in the response.")
                    return None
            else:
                print(f"Failed to upload file to IPFS: {response.text}")
                return None
    except Exception as e:
        logger.warning(f"Error while uploading file to IPFS: {e}. IPFS upload skipped.")
        return None
