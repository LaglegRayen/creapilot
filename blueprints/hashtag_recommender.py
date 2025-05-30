from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import os
from pathlib import Path
import requests
from api_requests import get_hashtag_id, get_top_media, get_recent_media
import json
from dotenv import load_dotenv

load_dotenv()

bp = Blueprint('hashtag_recommender', __name__)

def get_transcription(media_url):
    """
    Get transcription from the transcriber backend.
    """
    try:
        response = requests.post(
            'http://localhost:5001/transcribe',
            json={'reel_url': media_url}
        )
        if response.ok:
            return response.json()['transcription']
        return None
    except Exception as e:
        print(f"Error getting transcription: {e}")
        return None

def analyze_reel_components(transcript, caption, media_type):
    """
    Analyze different components of a reel and assign importance percentages.
    This is a placeholder for the n8n workflow integration.
    """
    # TODO: Replace with actual n8n workflow API call
    # For now, using a simple heuristic based on content length and presence
    components = {
        'hook': 0,
        'script': 0,
        'visuals': 0,
        'caption': 0,
        'music': 0
    }
    
    # Analyze hook (first 10 seconds of transcript)
    if transcript:
        hook_text = transcript.split('.')[0]  # First sentence
        if len(hook_text.split()) > 5:  # If hook has substantial content
            components['hook'] = 30
    
    # Analyze script (full transcript)
    if transcript and len(transcript.split()) > 20:
        components['script'] = 25
    
    # Analyze caption
    if caption and len(caption.split()) > 10:
        components['caption'] = 15
    
    # Visuals and music are always present in reels
    components['visuals'] = 20
    components['music'] = 10
    
    return components

def get_reel_analysis(media_items):
    """
    Process media items to get analysis including transcriptions and component importance.
    """
    analyzed_items = []
    
    for item in media_items:
        if item.get('media_type') == 'VIDEO':
            # Get transcription from transcriber backend
            transcript = get_transcription(item.get('media_url'))
            
            # Get component analysis
            analysis = analyze_reel_components(
                transcript=transcript,
                caption=item.get('caption', ''),
                media_type=item.get('media_type')
            )
            
            analyzed_items.append({
                'id': item['id'],
                'media_url': item.get('media_url'),
                'permalink': item.get('permalink'),
                'caption': item.get('caption', ''),
                'transcript': transcript or 'Transcription not available',
                'analysis': analysis
            })
    
    return analyzed_items

def get_recommended_hashtags(niche_hashtag, min_co_occur=5):
    """
    Get recommended hashtags based on co-occurrence with the input hashtag.
    
    Args:
        niche_hashtag (str): The input hashtag to find recommendations for
        min_co_occur (int): Minimum co-occurrence count to consider
        
    Returns:
        list: List of recommended hashtags with their co-occurrence counts
    """
    # Ensure hashtag has # prefix
    if not niche_hashtag.startswith('#'):
        niche_hashtag = '#' + niche_hashtag.lower()
    
    # Read co-occurrence matrix
    df_path = os.path.join('co-occur.csv')
    df = pd.read_csv(df_path)
    
    # Find all pairs where the input hashtag appears
    mask_a = df['hashtag_a'] == niche_hashtag
    mask_b = df['hashtag_b'] == niche_hashtag
    
    # Combine results from both columns
    recommendations = []
    
    # Get recommendations from hashtag_a column
    if mask_a.any():
        a_recommendations = df[mask_a][['hashtag_b', 'co_occur']].values.tolist()
        recommendations.extend(a_recommendations)
    
    # Get recommendations from hashtag_b column
    if mask_b.any():
        b_recommendations = df[mask_b][['hashtag_a', 'co_occur']].values.tolist()
        recommendations.extend(b_recommendations)
    
    # Sort by co-occurrence count and filter by minimum
    recommendations = [r for r in recommendations if r[1] >= min_co_occur]
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    # Format results
    formatted_recommendations = [
        {'hashtag': r[0], 'co_occur': r[1]} 
        for r in recommendations[:10]  # Return top 10 recommendations
    ]
    
    return formatted_recommendations

@bp.route('/hashtag-recommender', methods=['GET', 'POST'])
def hashtag_recommender():
    if request.method == 'POST':
        niche_hashtag = request.form.get('niche_hashtag', '').strip()
        if not niche_hashtag:
            return jsonify({'error': 'Please enter a hashtag'}), 400
        
        # Get hashtag ID
        hashtag_id = get_hashtag_id(niche_hashtag, os.getenv('USER_ID'), os.getenv('ACCESS_TOKEN'))
        if not hashtag_id:
            return jsonify({'error': 'Could not find hashtag'}), 404
        
        # Get top media
        media_items = get_top_media(hashtag_id, os.getenv('USER_ID'), os.getenv('ACCESS_TOKEN'))
        if not media_items:
            media_items = get_recent_media(hashtag_id, os.getenv('USER_ID'), os.getenv('ACCESS_TOKEN'))
        
        # Get hashtag recommendations
        recommendations = get_recommended_hashtags(niche_hashtag)
        
        # Get reel analysis
        analyzed_media = get_reel_analysis(media_items)
        
        return jsonify({
            'recommendations': recommendations,
            'media_analysis': analyzed_media
        })
        
    return render_template('hashtag_recommender/index.html') 