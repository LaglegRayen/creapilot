from flask import jsonify, request
from . import bp
import requests


@bp.route('/find-leads', methods=['POST'])
def find_leads():
    data = request.get_json()
    if not data or 'apollo_link' not in data:
        return jsonify({'error': 'Missing Apollo link parameter'}), 400
        
    apollo_link = data['apollo_link']
    
    N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/a35bbc5f-9902-4db7-bc85-fe49bbc873b3"

    payload = {
        "apollo_link": apollo_link,
        "category": "fitness",
        "country": "US"
    }

    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        response.raise_for_status()

        # Assuming JSON response from n8n
        result = response.json()
        return jsonify(result)

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to process Apollo link: {str(e)}'}), 500

    mock_leads = [
        {
            'name': 'John Doe',
            'email': 'john@example.com',
            'company': 'Tech Corp',
            'cold_email': f'Hi John,\n\nI noticed you work at Tech Corp...'
        }
    ]
    
    return jsonify({'leads': mock_leads}) 