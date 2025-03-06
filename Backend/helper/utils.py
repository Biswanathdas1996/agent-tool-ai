import os
import json
import pandas as pd

def get_config():
    config_path = os.path.join(os.path.dirname(__file__), '../string/const.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            gpt_config = json.load(file)
            return gpt_config
    except FileNotFoundError:
        print(f"Configuration file not found at {config_path}.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the configuration file at {config_path}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def convert_string_to_json(input_string):
    # Replace the newline character '\n' and other formatting issues to make it a valid JSON string
    input_string = input_string.replace("'", '"').replace('\n', '').strip()
    
    try:
        # Parse the string into JSON format
        json_data = json.loads(input_string)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error in decoding JSON: {str(e)}")
        return None

def convert_to_json(data):
    if not isinstance(data, list):
        print("Input data is not a list.")
        return data
    if not data or len(data) < 2:
        print("Input data is empty or does not contain enough rows.")
        return data
    
    headers = data[0]  # Extract the headers (first row)
    rows = data[1:]    # Extract the data rows
    
    # Create a list of dictionaries using headers as keys
    result = [dict(zip(headers, row)) for row in rows]
    
    return result
