from flask import Flask, render_template, jsonify
import requests
import time
import base64
from functools import lru_cache

app = Flask(__name__)

# Original Posts Data with Categories
original_posts = {
    'DIGITAL SERIES OF THE YEAR': {
        'base64_id': base64.b64encode(b'some_id_1').decode('utf-8'),
        'title': 'Digital Series 1'
    },
    'FANDOM OF THE YEAR': {
        'base64_id': base64.b64encode(b'some_id_2').decode('utf-8'),
        'title': 'Fandom 1'
    },
    'LOVETEAM OF THE YEAR': {
        'base64_id': base64.b64encode(b'some_id_3').decode('utf-8'),
        'title': 'Loveteam 1'
    },
    'MUSIC VIDEO OF THE YEAR': {
        'base64_id': base64.b64encode(b'some_id_4').decode('utf-8'),
        'title': 'Music Video 1'
    }
}

# Error Handling and Caching Decorator
@lru_cache(maxsize=32)
def fetch_facebook_data(post_id):
    try:
        response = requests.get(f'https://graph.facebook.com/v2.11/{post_id}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data: {e}')
        return None

@app.route('/')
def index():
    return render_template('dashboard.html', posts=original_posts)

@app.route('/refresh')
def refresh():
    rankings_data = {category: fetch_facebook_data(data['base64_id']) for category, data in original_posts.items()}
    return jsonify(rankings_data)

if __name__ == '__main__':
    app.run(debug=True)