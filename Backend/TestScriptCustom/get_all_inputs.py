import requests
from bs4 import BeautifulSoup
import json

def get_form_elements(html_content):
    try:
        
        soup = BeautifulSoup(html_content, 'html.parser')

        elements = []

        # Get all input tags
        for input_tag in soup.find_all('input'):
            element = {
                "tag": "input",
                "type": input_tag.get('type', 'text'),
                "name": input_tag.get('name'),
                "id": input_tag.get('id'),
                "value": input_tag.get('value')
            }
            elements.append(element)

        # Get all select tags
        for select_tag in soup.find_all('select'):
            options = []
            for option in select_tag.find_all('option'):
                option_data = {
                    "label": option.text.strip(),   # Visible text
                    "value": option.get('value')    # Value attribute
                }
                options.append(option_data)

            element = {
                "tag": "select",
                "name": select_tag.get('name'),
                "id": select_tag.get('id'),
                "options": options
            }
            elements.append(element)

        # Get all textarea tags
        for textarea_tag in soup.find_all('textarea'):
            element = {
                "tag": "textarea",
                "name": textarea_tag.get('name'),
                "id": textarea_tag.get('id'),
                "value": textarea_tag.text.strip(),
                "placeholder": textarea_tag.get('placeholder')
            }
            elements.append(element)

        return elements

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []


