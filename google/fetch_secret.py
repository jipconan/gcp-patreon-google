import json
from google.cloud import secretmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("google/.env")

def fetch_secret():
    client = secretmanager.SecretManagerServiceClient()

    # Secret and project ID from environment variables
    secret_name = os.getenv("GOOGLE_SECRET_NAME")
    project_number = os.getenv("GOOGLE_PROJECT_NUMBER")

    secret_key = f"projects/{project_number}/secrets/{secret_name}/versions/latest"

    try:
        # Access the secret version
        response = client.access_secret_version(name=secret_key)
        secret_data = response.payload.data.decode("UTF-8")
        
        # Parse the JSON data into a dictionary
        secret_dict = json.loads(secret_data)
        return secret_dict

    except Exception as e:
        print(f"Error accessing secret: {e}")
        return None
