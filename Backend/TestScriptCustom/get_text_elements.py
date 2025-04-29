import requests
from bs4 import BeautifulSoup
import json

def get_text_elements_from_url(html_content):
    try:
       
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Common text-related tags
        text_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'a', 'li', 'div', 'strong', 'em', 'b', 'i']

        elements = []
        
        for tag in soup.find_all(text_tags):
            element_info = {
                'tag': tag.name,
                'text': tag.get_text(strip=True),
                'id': tag.get('id'),
                'class': tag.get('class')
            }
            elements.append(element_info)
        
        return elements
    
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None



