import requests
from flask import jsonify, request
from . import bp

@bp.route('/research', methods=['POST'])
def research_products():
    data = request.get_json()
    if not data or 'keyword' not in data:
        return jsonify({'error': 'Missing keyword parameter'}), 400
        
    keyword = data['keyword']
    
    # TODO: Replace with actual n8n webhook URL
    n8n_webhook_url = "http://localhost:5678/webhook/product-research"
    
    try:
        response = requests.post(n8n_webhook_url, json={'keyword': keyword})
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to fetch product data: {str(e)}'}), 500 