import os
from github_fetcher import get_java_files
from code_analyzer import analyze_code
from groq_suggestions import get_code_suggestions
from typing import List, Dict
import json

def generate_report(issues: List[Dict], suggestions: str, output_file: str):
    """Generate a detailed report of code review findings"""
    with open(output_file, 'w') as f:
        f.write("# Code Review Report\n\n")
        
        # Write issues
        f.write("## Issues Found\n\n")
        for issue in issues:
            f.write(f"- Line {issue['line']}: {issue['description']} (Type: {issue['type']})\n")
        
        # Write AI suggestions
        f.write("\n## AI Suggestions\n\n")
        f.write(suggestions)

def main():
    # Get environment variables
    github_token = os.getenv('GITHUB_TOKEN')
    groq_api_key = os.getenv('GROQ_API_KEY')
    
    if not github_token or not groq_api_key:
        raise ValueError("Please set GITHUB_TOKEN and GROQ_API_KEY environment variables")
    
    # Get repository URL from user
    repo_url = "https://github.com/Hari7467/tester"
    
    try:
        # Fetch Java files
        print("Fetching Java files...")
        java_files = get_java_files(repo_url, github_token)
        
        for file_info in java_files:
            print(f"\nAnalyzing {file_info['path']}...")
            
            # Analyze code
            issues = analyze_code(file_info['content'])
            
            # Get AI suggestions
            print("Getting AI suggestions...")
            suggestions = get_code_suggestions(file_info['content'], groq_api_key)
            
            # Generate report
            output_file = f"report_{file_info['path'].replace('/', '_')}.md"
            generate_report(issues, suggestions, output_file)
            print(f"Report generated: {output_file}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()