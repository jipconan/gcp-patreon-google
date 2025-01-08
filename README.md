# GCP Patreon + Google BigQuery Integration

## Overview

This project is a serverless application designed to automate the retrieval of impression count data from all posts in a Patreon campaign and store the data in Google BigQuery.

## Functionality

The application performs the following key functions:

1. **Fetch Patreon Posts**  
   Retrieves all posts from a specified Patreon campaign using the Patreon API, focusing exclusively on `impression_counts` data.

2. **Store in Google BigQuery**  
   Consolidates the impression_counts data and stores the processed data in a structured format in Google BigQuery.

3. **Error Handling and Logging**  
   Logs errors encountered during API calls (e.g., authentication failures or data submission issues) to Google Cloud Logging, enabling traceability and troubleshooting.

## Usage

This Google Cloud Function is triggered on a daily schedule using Google Cloud Scheduler, ensuring the latest impression_counts from all posts are captured and stored in BigQuery. Users can adjust the trigger schedule by modifying the configuration in the Google Cloud Console.

## Setup & Deployment

I will update here real soon!
