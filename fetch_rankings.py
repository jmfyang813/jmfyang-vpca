import requests
import datetime
import pytz
import time
import json
from flask import Flask, render_template_string, request
import os

# Facebook API credentials
fb_dtsg = 'YOUR_FB_DTSG'
lsd = 'YOUR_LSD'
jazoest = 'YOUR_JAZOEST'

# Headers configuration
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/json',
}

# Posts dictionary (example categories and IDs)
posts = {
    'Category1': [1234567890],
    'Category2': [1234567891],
}

# Flask app setup
app = Flask(__name__)

# Cached data
cached_data = {}

# Template for rankings dashboard
HTML_TEMPLATE = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rankings Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
<h1>Rankings Dashboard</h1>
<table>
    <tr><th>Category</th><th>Rank</th></tr>
    {% for category, rank in cached_data.items() %}
    <tr><td>{{ category }}</td><td>{{ rank }}</td></tr>
    {% endfor %}
</table>
<form method="post">
    <button type="submit">Refresh</button>
</form>
</body>
</html>
'''

# Function to fetch GraphQL data
def fetch_graphql(query):
    response = requests.post('https://graph.facebook.com/graphql', headers=headers, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Error fetching GraphQL data: {response.status_code}')

# Function to fetch and generate post data
def fetch_and_generate():
    for category, ids in posts.items():
        # Fetch data for each post ID
        for post_id in ids:
            query = f'{{ post(id: {post_id}) {{ title, rank }} }}'
            data = fetch_graphql(query)
            if data:
                # Assume JSON structure is returned
                rank = data['data']['post']['rank']
                cached_data[category] = rank

# Flask route for index
@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

# Flask route for refresh
@app.route('/', methods=['POST'])
def refresh():
    fetch_and_generate()
    return render_template_string(HTML_TEMPLATE)

# Main execution block
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)