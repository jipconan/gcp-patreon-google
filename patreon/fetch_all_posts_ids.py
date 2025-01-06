import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

load_dotenv("patreon/.env")

# Function to fetch all post IDs from Patreon within a date range
def fetch_all_posts_ids(startYear):
    access_token = os.getenv("PATRON_API_KEY")
    campaign_id = os.getenv("PATRON_CAMPAIGN_ID")
    post_ids = []

    base_url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{campaign_id}/posts"
    params = {
        "fields[post]": "url,published_at",  # Fetch both 'url' and 'published_at'
        "page[count]": "10",                # Adjust for pagination size if needed
        "sort": "-published_at"             # Sort by published date in descending order
    }

    # Date range for filtering
    start_date = datetime(startYear, 1, 1, tzinfo=timezone.utc)
    end_date = datetime.now(timezone.utc)

    # Initial API call
    response = requests.get(base_url, headers={"Authorization": f"Bearer {access_token}"}, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch posts: {response.content}")

    # Process pages
    while response.status_code == 200:
        data = response.json()
        
        # Filter posts based on the published_at date
        for post in data.get('data', []):
            published_at = post['attributes'].get('published_at')
            if published_at:
                post_date = datetime.fromisoformat(published_at.rstrip('Z')).replace(tzinfo=timezone.utc)
                if start_date <= post_date <= end_date:
                    post_id = post['attributes']['url'].split('/')[-1].split('-')[-1]  # Extract numeric ID
                    post_ids.append(post_id)
        
        next_page = data.get('links', {}).get('next')
        if not next_page:
            break  # No more pages, exit the loop

        # Fetch the next page
        response = requests.get(next_page, headers={"Authorization": f"Bearer {access_token}"})

    return post_ids  # Returning the filtered array of post IDs

# Example usage
# if __name__ == '__main__':
#     post_ids = fetch_all_posts_ids()
#     print(f"Total number of post IDs fetched: {len(post_ids)}")
#     print("Post IDs Array:")
#     print(post_ids)
