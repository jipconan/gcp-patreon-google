import os
from google.cloud import bigquery
from dotenv import load_dotenv
# from google.fetch_secret import fetch_secret
# from google.create_temp_key_file import create_temp_key_file
from datetime import datetime, timezone

# Load environment variables
load_dotenv("google/.env")

# Set the event timestamp
event_timestamp = datetime.now(timezone.utc).replace(microsecond=0).strftime('%Y-%m-%d %H:%M:%S UTC')

# Fetch the service account key (returns a dictionary)
# service_account_key = fetch_secret()

def add_data_to_bigquery(fetched_data):
    # # Create a temporary service account JSON file
    # temp_key_file = create_temp_key_file(service_account_key)

    # # Set GOOGLE_APPLICATION_CREDENTIALS to the temp file path
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_key_file

    # Initialize BigQuery client
    client = bigquery.Client()

    # Correct dataset and table IDs
    dataset_id = os.getenv("GOOGLE_DATASET_ID")
    table_id = os.getenv("GOOGLE_TABLE_ID")
    table_ref = client.dataset(dataset_id).table(table_id)

    # Prepare rows to insert from fetched data
    rows_to_insert = []
    for post in fetched_data:
        rows_to_insert.append({
            "event_timestamp": event_timestamp, 
            "id": post.get("post_id"),
            "title": post.get("post_title"),
            "post_url": post.get("post_url"),
            "impression_count": post.get("impression_count"),
            "sales": post.get("sales_count"),
            "earnings": post.get("earnings")
        })


    # Insert rows
    errors = client.insert_rows_json(table_ref, rows_to_insert)
    if errors:
        print("Encountered errors while inserting rows:", errors)
    else:
        print("Data inserted successfully.")

    # Clean up the temporary file
    # os.remove(temp_key_file)

# if __name__ == "__main__":
#     insert_data_to_bigquery()


