from flask import  request, jsonify
import requests

from TestScriptCustom.get_text_elements import get_text_elements_from_url
from TestScriptCustom.get_media import get_media_from_url
from TestScriptCustom.get_all_inputs import get_form_elements



def merge_json_outputs(text_data, media_data, form_data):
    # Create a final combined dictionary
    final_output = {
        'text_elements': text_data,
        'media_elements': media_data,
        'form_elements': form_data
    }
    return final_output


def extract_elements():
    data = request.get_json()

    if not data or 'url' not in data:
        return jsonify({'error': 'Missing URL in request'}), 400

    url = data['url']
    html = data['html']

    html_content = None


    if(url):
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
    else:
        html_content = html


    try:
        # Call your existing functions
        text_data = get_text_elements_from_url(html_content)
        media_data = get_media_from_url(html_content, url)
        form_data = get_form_elements(html_content)

        # Merge everything
        final_output = merge_json_outputs(text_data, media_data, form_data)

        return jsonify(final_output), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def render_html_extract_elements(app):
    app.add_url_rule('/html_upload', 'extract_elements_api', extract_elements, methods=['POST'])
    return app
