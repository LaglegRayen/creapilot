from flask import jsonify, request
from . import bp

@bp.route('/query', methods=['POST'])
def process_query():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'error': 'Missing question parameter'}), 400
        
    question = data['question']
    
    # TODO: Implement actual SQL generation and execution
    # For now, return mock data
    mock_results = {
        'sql': 'SELECT * FROM products WHERE category = "electronics"',
        'results': [
            {'id': 1, 'name': 'Laptop', 'price': 999.99},
            {'id': 2, 'name': 'Smartphone', 'price': 699.99}
        ]
    }
    
    return jsonify(mock_results) 