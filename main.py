import json
from flask import Flask, request, jsonify
import logging
from patreon.fetch_all_post_ids import fetch_all_post_ids
from patreon.fetch_impression import fetch_impression
from google.add_data_to_google_sheet import add_data_to_google_sheet
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)

load_dotenv("patreon/.env")

# Initialize Flask app
app = Flask(__name__)

# Main function handler for local Flask server
@app.route('/main', methods=['POST'])
def main():
    try:
        logging.info("Function triggered.")

        # Fetch all post IDs
        post_ids = fetch_all_post_ids()

        # Declare Patreon session ID
        session_id = os.getenv("PATRON_SESSION_ID")

        # List to store post IDs and impressions
        impression_data = []

        # Fetch impressions for each post and store the data
        for post_id in post_ids:
            impression = fetch_impression(post_id, session_id)
            if impression:
                impression_data.append(impression)

        # Add the data to Google Sheets
        if impression_data:
            sheet_id = add_data_to_google_sheet(impression_data)
            logging.info(f"Data added to Google Sheet with ID: {sheet_id}")
            return jsonify({"message": f"Data added to Google Sheet with ID: {sheet_id}"}), 200

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Run Flask locally
if __name__ == '__main__':
    app.run(debug=True)