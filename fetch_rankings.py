import requests
from datetime import datetime

# Function to fetch Facebook post data

def fetch_facebook_data(page_id, access_token):
    url = f'https://graph.facebook.com/v12.0/{page_id}/posts'
    params = {'access_token': access_token}
    response = requests.get(url, params=params)
    return response.json()

# Function to generate HTML report

def generate_html_report(posts):
    html_content = '<html><head><title>Facebook Post Report</title></head><body>'
    html_content += '<h1>Facebook Post Report</h1>'
    html_content += '<table border="1"><tr><th>Post ID</th><th>Message</th><th>Created Time</th></tr>'
    for post in posts:
        html_content += f'<tr><td>{post.get("id", "N/A")}</td><td>{post.get("message", "N/A")}</td><td>{post.get("created_time", "N/A")}</td></tr>'
    html_content += '</table></body></html>'
    return html_content

# Example usage
if __name__ == '__main__':
    page_id = 'your_page_id'
    access_token = 'your_access_token'
    posts = fetch_facebook_data(page_id, access_token)
    report = generate_html_report(posts)
    with open('report.html', 'w') as file:
        file.write(report)
    print('HTML report generated!')
