from flask import Blueprint, request, jsonify
from blueprints.video_ideas.ig_scraper import fetch_instagram_data

bp = Blueprint('video_ideas', __name__)

@bp.route('/', methods=['POST'])
def generate_video_ideas():
    
    data = request.get_json() or request.form
    platform = data.get('platform')
    topic = data.get('topic')
    if not platform or not topic:
        return jsonify({'error': 'Platform and topic are required'}), 400


    # Instagram-specific scraping
    if platform.lower() == 'instagram':
        try:
            suggestions, hashtag_details, ideas = fetch_instagram_data(topic)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        hashtags = [f'#{s}' for s in suggestions]
        return jsonify({'hashtags': hashtags, 'hashtag_details': hashtag_details, 'ideas': ideas}), 200

    # Fallback for other platforms
    hashtags = [f'#{platform.lower()}{i}' for i in range(1, 11)]
    return jsonify({'hashtags': hashtags}), 200 