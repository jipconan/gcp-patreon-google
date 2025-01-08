import json
from flask import Flask, request, jsonify
import logging
from patreon.fetch_all_posts_ids import fetch_all_posts_ids
from patreon.fetch_post_data import fetch_post_data
# from google.add_data_to_google_sheet import add_data_to_google_sheet
import os
from dotenv import load_dotenv
from google.add_data_to_bigquery import add_data_to_bigquery

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

        # Fetch all post IDs fetch_all_posts_ids(startYear)
        post_ids = fetch_all_posts_ids(2024)

        # Declare Patreon session ID
        session_id = os.getenv("PATRON_SESSION_ID")

        # List to store post IDs and impressions
        fetched_data = []

        # Fetch post data for each post and store the data
        for post_id in post_ids:
            post_data = fetch_post_data(post_id, session_id)
            if post_data:
                fetched_data.append(post_data)

        # Add the data to Google Sheets
        # if fetched_data:
        #     sheet_id = add_data_to_google_sheet(fetched_data)
        #     logging.info(f"Data added to Google Sheet with ID: {sheet_id}")
        #     return jsonify({"message": f"Data added to Google Sheet with ID: {sheet_id}"}), 200

        # Add the data to Big Query
        if fetched_data:
            add_data_to_bigquery(fetched_data)
            logging.info("Data added to Big Query.")
            return jsonify({"message": "Data added to Big Query."}), 200

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Run Flask locally
# if __name__ == '__main__':
#     app.run(debug=True)