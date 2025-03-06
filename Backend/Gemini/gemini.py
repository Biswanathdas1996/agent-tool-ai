import os
import google.generativeai as genai
from secretes.secrets import GEMINI_API_KEY, GOOGLE_MODEL_NAME

def configure_genai(api_key, model_name):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name)

def set_environment_variable(key, value):
    try:
        os.environ[key] = value
    except Exception as e:
        print(f"Error setting environment variable: {e}")

def call_gemini(model, prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.replace('```', '').replace('gherkin', '')
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    model = configure_genai(GEMINI_API_KEY, GOOGLE_MODEL_NAME)
    set_environment_variable("OPENAI_API_KEY", GEMINI_API_KEY)
