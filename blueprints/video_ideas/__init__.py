from flask import Blueprint, request, jsonify
import json
import numpy as np
import tensorflow as tf
from transformers import pipeline

# Seed numpy and TensorFlow for deterministic AI output
np.random.seed(42)
tf.random.set_seed(42)
# Initialize text-generation pipeline using TensorFlow backend
generator = pipeline("text-generation", model="gpt2", framework="tf")

bp = Blueprint('video_ideas', __name__)

@bp.route('/', methods=['POST'])
def generate_video_ideas():
    data = request.get_json() or request.form
    topic = data.get('topic')
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    prompt = (
        f"Generate 5 high-potential YouTube video ideas for the niche '{topic}'. "
        "For each idea, provide title, one-line dein vien, and why it works. "
        "Respond in JSON format as an array of objects with fields title, description, value."
    )
    try:
        # Generate text using TensorFlow backend
        response = generator(
            prompt,
            max_new_tokens=200,
            do_sample=True,
            temperature=0.7,
            return_full_text=False,
            num_return_sequences=1,
            pad_token_id=generator.tokenizer.eos_token_id
        )
        generated = response[0]['generated_text'].strip()
        ideas = json.loads(generated)
    except Exception as e:
        # Return the error message to help debugging
        return jsonify({'error': f"AI generation failed: {str(e)}"}), 500
    return jsonify({'ideas': ideas}), 200 