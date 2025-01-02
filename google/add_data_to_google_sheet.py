from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv("google/.env")

# Path to your service account JSON file
SERVICE_ACCOUNT_FILE = 'google/fifth-bonbon-442814-r6-d9648c69b7f5.json'

# Define the necessary scopes for Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets'
]

# Authenticate using the service account
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
sheets_service = build('sheets', 'v4', credentials=credentials)

def add_data_to_google_sheet(impression_counts):
    # Use an existing Google Sheet ID from environment variables
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        print("Error: GOOGLE_SHEET_ID is not set.")
        return None

    # Log the impression_counts to see its structure
    print("[LOG] impression_counts:", impression_counts)

    # Get the current date and time
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d")

    # Prepare the data to append (including date and time)
    try:
        values = [[formatted_time, item['post_id'], item['post_url'], item['impression_count']] for item in impression_counts]
    except KeyError as e:
        print(f"Error: Missing key {e} in impression_counts data.")
        return None

    # Append the data to the Google Sheet
    body = {
        'values': values,
    }

    try:
        response = sheets_service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range='Sheet1',  # Assuming data is on the first sheet
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',  # Insert data as new rows
            body=body
        ).execute()
        print(f"Data appended to the Google Sheet: {response}")
    except Exception as e:
        print(f"Error occurred while appending data to the Google Sheet: {e}")
        return None

    return sheet_id
