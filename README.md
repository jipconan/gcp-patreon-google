# GCP Patreon + Google Sheets Integration

## Overview

This project is a serverless application designed to automate the retrieval of impression count data from all posts in a Patreon campaign and store the data in a Google Sheets document saved to Google Drive.

## Functionality

The application performs the following key functions:

1. **Fetch Patreon Posts**  
   Retrieves all posts from a specified Patreon campaign using the Patreon API, focusing exclusively on `impression_counts` data.

2. **Generate Google Sheet**  
   Consolidates the `impression_counts` data and generates a new Google Sheet, storing the processed data in a structured format.

3. **Save to Google Drive**  
   Saves the generated Google Sheet to a specific Google Drive folder, as specified by the folder ID.

4. **Error Handling and Logging**  
   Logs errors encountered during API calls (e.g., authentication failures or data submission issues) to Google Cloud Logging, enabling traceability and troubleshooting.

## Usage

This Google Cloud Function is triggered on a daily schedule using Google Cloud Scheduler, ensuring the latest `impression_counts` from all posts are captured and saved. Users can adjust the trigger schedule by modifying the configuration in the Google Cloud Console.

## Setup & Deployment

I will update here real soon!
