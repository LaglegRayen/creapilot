from flask import jsonify, request
from . import bp
import pandas as pd
import os
import requests
from datetime import datetime

# Instagram API credentials
USER_ID = '17841407434839041'
ACCESS_TOKEN = 'EAA1QFt7XvPoBOZCihik3zo1EAqSFXyXDUxKlS2UsZBmkSmKlHSzRzwMK4KWimciH3yreIrHweALuuM73g3KO9ZCvrysouBZA7y8a2uuVMz0X7f6yeqCgmBtOE2ZCBTMOhGBhfC7W3HaM1wRQQFOOyUKN2VcY3OPMGO25zmZAFSBhh9LahUwZCyV'

def get_hashtag_id(hashtag_name):
    """Get Instagram hashtag ID from our database or API"""
    df_path = os.path.join('hashtag co-occurrence matrix', 'hashtag_id_df.csv')
    df = pd.read_csv(df_path)
    
    if hashtag_name in df['hashtag_name'].values:
        id = df.loc[df['hashtag_name'] == hashtag_name, 'id'].values[0]
        print(f"Found existing ID for #{hashtag_name}")
    else:
        url = f"https://graph.facebook.com/v22.0/ig_hashtag_search"
        params = {
            'user_id': USER_ID,
            'q': hashtag_name,
            'access_token': ACCESS_TOKEN
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'data' in data and data['data']:
            id = data['data'][0]['id']
            update_hashtag_id_df(hashtag_name, id)
        else:
            id = None
    
    return id

def get_top_media(hashtag_id):
    """Get top media for a hashtag"""
    url = f"https://graph.facebook.com/v19.0/{hashtag_id}/top_media"
    params = {
        'user_id': USER_ID,
        'fields': 'id,caption,media_type,media_url,permalink',
        'access_token': ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data.get('data', [])

def update_hashtag_id_df(hashtag_name, id):
    """Update our hashtag ID database"""
    df_path = os.path.join('hashtag co-occurrence matrix', 'hashtag_id_df.csv')
    df = pd.read_csv(df_path)
    if hashtag_name not in df['hashtag_name'].values:
        df.loc[len(df)] = {'hashtag_name': hashtag_name, 'id': id}
        print(f"Added new hashtag: {hashtag_name} with ID: {id}")
        df.sort_values(by='hashtag_name', inplace=True)
        df.to_csv(df_path, index=False)

def get_co_occurring_hashtags(hashtag):
    """
    Get co-occurring hashtags from the co-occurrence matrix
    Returns top hashtags that frequently appear with the input hashtag
    """
    try:
        # Read the co-occurrence matrix
        co_occur_df = pd.read_csv('co-occur.csv')
        
        # Find the hashtag's row
        hashtag_row = co_occur_df[co_occur_df['hashtag'] == hashtag]
        if hashtag_row.empty:
            return []
            
        # Get top 10 co-occurring hashtags with their frequencies
        co_occurring = hashtag_row.iloc[0, 1:].sort_values(ascending=False).head(10)
        
        # Convert to list of dictionaries with hashtag and frequency
        result = [
            {
                'hashtag': tag,
                'frequency': int(freq),
                'percentage': round((freq / co_occurring.max()) * 100, 1)
            }
            for tag, freq in co_occurring.items()
            if freq > 0
        ]
        
        return result
    except Exception as e:
        print(f"Error getting co-occurring hashtags: {e}")
        return []

@bp.route('/scrape', methods=['POST'])
def scrape_social_media():
    data = request.get_json()
    if not data or 'keyword' not in data:
        return jsonify({'error': 'Missing keyword parameter'}), 400
        
    keyword = data['keyword']
    
    try:
        # Get co-occurring hashtags
        co_occurring_hashtags = get_co_occurring_hashtags(keyword)
        
        # Get media for main keyword and co-occurring hashtags
        all_media = []
        
        # Get media for main keyword
        main_hashtag_id = get_hashtag_id(keyword)
        if main_hashtag_id:
            main_media = get_top_media(main_hashtag_id)
            for media in main_media:
                media['source_hashtag'] = keyword
            all_media.extend(main_media)
        
        # Get media for co-occurring hashtags
        for hashtag in co_occurring_hashtags:
            hashtag_id = get_hashtag_id(hashtag)
            if hashtag_id:
                hashtag_media = get_top_media(hashtag_id)
                for media in hashtag_media:
                    media['source_hashtag'] = hashtag
                all_media.extend(hashtag_media)
        
        return jsonify({
            'main_keyword': keyword,
            'co_occurring_hashtags': co_occurring_hashtags,
            'media': all_media
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch media: {str(e)}'}), 500 