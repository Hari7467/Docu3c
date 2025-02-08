import requests
from typing import List, Dict
import base64

def get_java_files(repo_url: str, github_token: str) -> List[Dict]:
    # Extract owner and repo from URL
    parts = repo_url.strip('/').split('/')
    owner, repo = parts[-2], parts[-1]
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Get repository contents
    api_url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1'
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    
    java_files = []
    tree = response.json().get('tree', [])
    
    for item in tree:
        if item['path'].endswith('.java'):
            # Get file content
            file_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{item["path"]}'
            file_response = requests.get(file_url, headers=headers)
            file_response.raise_for_status()
            
            content = base64.b64decode(file_response.json()['content']).decode('utf-8')
            java_files.append({
                'path': item['path'],
                'content': content
            })
    
    return java_files