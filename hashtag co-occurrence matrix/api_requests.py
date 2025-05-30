import os
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
OUTPUT_FILE = 'instagram_api_response.txt'
import json
USER_ID = '17841407434839041'
ACCESS_TOKEN = 'EAA1QFt7XvPoBOZCihik3zo1EAqSFXyXDUxKlS2UsZBmkSmKlHSzRzwMK4KWimciH3yreIrHweALuuM73g3KO9ZCvrysouBZA7y8a2uuVMz0X7f6yeqCgmBtOE2ZCBTMOhGBhfC7W3HaM1wRQQFOOyUKN2VcY3OPMGO25zmZAFSBhh9LahUwZCyV'



# def get_hashtag_id(hashtag_name, user_id, access_token):
#     print(1)
#     df_path = os.path.join('hashtag co-occurrence matrix', 'hashtag_id_df.csv')
#     df = pd.read_csv(df_path)
#     if hashtag_name in df['hashtag_name'].values:
#         id = df.loc[df['hashtag_name']==hashtag_name,'id'].values[0]
#         print(f"already have the id of #{hashtag_name}")
#     else:
#         url = f"https://graph.facebook.com/v22.0/ig_hashtag_search"
#         params = {
#             'user_id': user_id,
#             'q': hashtag_name,
#             'access_token': access_token
#         }
#         response = requests.get(url, params=params)
#         data = response.json()
#         print("Hashtag ID response:", data)
#         if 'data' in data and data['data']:
#             id = data['data'][0]['id']
#             update_hashtag_id_df(hashtag_name,id)
#         else:
#             id = None
#       
#     return id

# def get_top_media(hashtag_id,user_id, access_token):
#     print(2)
#     url = f"https://graph.facebook.com/v19.0/{hashtag_id}/top_media"
#     params = {
#         'user_id': user_id,
#         'fields': 'id,caption,media_type,media_url,permalink',
#         'access_token': access_token
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     print("Top Media response:", data)
#     return data.get('data', [])




def log_rate_limit_info(response):
    headers = response.headers

    # Parse X-App-Usage safely
    app_usage_str = headers.get('x-app-usage')
    if app_usage_str:
        app_usage = json.loads(app_usage_str)
        call_count = app_usage.get('call_count', 'N/A')
        total_cputime = app_usage.get('total_cputime', 'N/A')
        total_time = app_usage.get('total_time', 'N/A')
    else:
        call_count = total_cputime = total_time = 'N/A'

    # Error info
    www_auth = headers.get('WWW-Authenticate', '')
    limit_status = "LIMIT EXCEEDED" if "invalid_request" in www_auth else "OK"

    # IDs
    request_id = headers.get('x-fb-request-id', 'N/A')
    trace_id = headers.get('x-fb-trace-id', 'N/A')

    log_line = (
        f"[{datetime.now().isoformat()}] Request-ID: {request_id}, Trace-ID: {trace_id}\n"
        f"X-App-Usage: call_count={call_count}%, total_cputime={total_cputime}, total_time={total_time}\n"
        f"Rate Limit Status: {limit_status}\n"
        f"Error Message: {www_auth}\n"
        "---------------------------------------\n"
    )

    with open("api_rate_limit_log.txt", "a") as f:
        f.write(log_line)


def get_hashtag_id(hashtag_name, user_id, access_token):
    print(1)
    df_path = os.path.join('hashtag co-occurrence matrix', 'hashtag_id_df.csv')
    df = pd.read_csv(df_path)
    
    if hashtag_name in df['hashtag_name'].values:
        id = df.loc[df['hashtag_name'] == hashtag_name, 'id'].values[0]
        print(f"already have the id of {hashtag_name}")
    else:
        url = f"https://graph.facebook.com/v22.0/ig_hashtag_search"
        params = {
            'user_id': user_id,
            'q': hashtag_name,
            'access_token': access_token
        }
        response = requests.get(url, params=params)
        data = response.json()
        print("Hashtag ID response:", data)
        
        log_rate_limit_info(response)
        
        if 'data' in data and data['data']:
            id = data['data'][0]['id']
            update_hashtag_id_df(hashtag_name, id)
        else:
            id = None
        
    return id




def get_top_media(hashtag_id, user_id, access_token):
    print(2)
    url = f"https://graph.facebook.com/v19.0/{hashtag_id}/top_media"
    params = {
        'user_id': user_id,
        'fields': 'id,caption,media_type,media_url,permalink',
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    data = response.json()
    # print("Top Media response:", data)
    
    log_rate_limit_info(response)
    return data.get('data', [])

# print(get_top_media(17843710354061170,USER_ID,ACCESS_TOKEN))


def get_recent_media(hashtag_id,user_id, access_token):
    url = f"https://graph.facebook.com/v19.0/{hashtag_id}/recent_media"
    params = {
        'user_id': user_id,
        'fields': 'id,caption,media_type,media_url,permalink',
        'access_token': access_token
    }
    response = requests.get(url, params=params)
    data = response.json()
    print("Recent Media response:", data)
    log_rate_limit_info(response)
    return data.get('data', [])






def add_post_id(post):
    df_path = os.path.join('hashtag co-occurrence matrix', 'posts_df.csv')
    df = pd.read_csv(df_path)
    
    # Convert post['id'] to string to ensure consistent comparison
    post_id = str(post['id'])
    
    # Check if post ID exists
    if post_id not in df['id'].astype(str).values:
        df.loc[len(df)] = {'id': post_id}
        print(f'Added new post ID: {post_id}')
        df.to_csv(df_path, index=False)
    else:
        print(f'Post ID {post_id} already exists in database')


def update_hashtag_id_df(hashtag_name,id):
    df_path = os.path.join('hashtag co-occurrence matrix', 'hashtag_id_df.csv')
    df = pd.read_csv(df_path)
    if hashtag_name not in df['hashtag_name'].values:

        df.loc[len(df)] = {'hashtag_name': hashtag_name, 'id': id}
        print(f"Added new hashtag: {hashtag_name} with ID: {id}")
        df.sort_values(by='hashtag_name', inplace=True)
    df.to_csv(df_path, index=False)



def log_to_file(title, data):
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*40}\n{title}\n{'='*40}\n")
        f.write(f"{data}\n\n")
        






# if __name__ == "__main__":
#     hashtag_id = get_hashtag_id(HASHTAG_NAME)
#     if hashtag_id:
#         top_media = get_top_media(hashtag_id)
#         for media in top_media:
#             print(f"\nMedia ID: {media['id']}")
#             print(f"Type: {media['media_type']}")
#             print(f"URL: {media['media_url']}")
#             print(f"Permalink: {media['permalink']}")
#             print(f"Caption: {media.get('caption', 'No caption')}")
#             log_to_file(f"Media ID: {media['id']}", 
#                         f"""Type: {media['media_type']}\n
#                         URL: {media['media_url']}\n
#                         Permalink: {media['permalink']}\n
#                         Caption: {media.get('caption', 'No caption')}""")
#     else:
#         print("Hashtag not found.")