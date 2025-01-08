import requests
import json

def fetch_post_data(post_id, session_id):
    base_url = f"https://www.patreon.com/api/posts/{post_id}"
    params = {
        'fields[post]': 'audio,comment_count,commenter_count,impression_count,insights_last_updated_at,like_count,monetization_ineligibility_reason,post_metadata,post_type,published_at,title,video,view_count',
        'fields[insights]': 'earnings,sales,currency_code',
        'fields[content-unlock-option]': 'content_unlock_type',
        'fields[product-variant]': 'price_cents,currency_code,is_hidden,published_at_datetime',
        'include': 'native_video_insights,drop,content_unlock_options.product_variant.insights',
        'json-api-version': '1.0',
        'json-api-use-default-includes': 'false'
    }
    headers = {
        'Cookie': f'session_id={session_id};',
        'Content-Type': 'application/json',
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()

            # Log the full response for debugging
            # print(json.dumps(data, indent=2))

            # Check if there are monetization options
            # if not data['data']['relationships']['content_unlock_options']['data']:
            #     print(f"[INFO] Post {post_id} has no monetization options. Skipping.")
            #     return None

            # Initialize variables for sales and earnings to 0
            sales_count = 0
            earnings = 0

            # Extract insights for sales and earnings data
            for item in data.get('included', []):
                if item.get('type') == 'insights':
                    sales_count = item.get('attributes', {}).get('sales', 0)  # Will be 0 if not present
                    earnings = item.get('attributes', {}).get('earnings', 0)  # Will be 0 if not present
                    break  # Stop after the first insights item (as there should only be one)

            # Extract impression count, post title, and post URL
            impression_count = data['data']['attributes'].get('impression_count', 0)
            post_title = data['data']['attributes'].get('title', 'Untitled')
            post_url = data['links']['self']

            # Log the result
            log_data = {
                "post_id": post_id,
                "post_title": post_title,
                "post_url": post_url,
                "impression_count": impression_count,
                "sales_count": sales_count,
                "earnings": earnings
            }
            print(f"[LOG] {json.dumps(log_data, indent=2)}")
            return log_data
        else:
            print(f"[ERROR] Status Code: {response.status_code}")
            print(f"[DEBUG] Response: {response.text}")
    except Exception as e:
        print(f"[EXCEPTION] {e}")

    return None
