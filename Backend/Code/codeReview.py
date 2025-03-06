import os
import openai

from Gemini.gemini import call_gemini

from config import TECHNOLOGY

# Define paths
INPUT_FOLDER = "./Code/src_code"
OUTPUT_FOLDER = "./Code/report"

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def set_openai_api_key():
    openai.api_key = os.environ["OPENAI_API_KEY"]

def analyze_code(file_path):
    """
    Analyze the code using OpenAI API and return a quality report.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code_content = file.read()
        prompt = f"""
                    Analyze the following code for quality issues, best practices, correctness, and security. Provide detailed feedback and recommendations in an ordered list, one by one. Format the output as a well-structured HTML report.

                    Code:
                    {code_content}
                    \n\n
                    Output format:\n
                    - Provide details documentations of the code.\n
                    - The report should be structured in an HTML format with a `<head>` containing metadata and a `<body>` with a title, introduction, Code documentations and the ordered list of recommendations.\n
                    - Each recommendation in the ordered list should have a brief description followed by the suggested improvement or best practice.\n
                    - Ensure the HTML is properly formatted with appropriate sections, headings, and lists.\n
                    """
        if TECHNOLOGY != "GEMINI":
            print("Using OpenAI")
            set_openai_api_key()
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a code quality analyzer."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['choices'][0]['message']['content']
        else:
            print("Using Gemini")
            return call_gemini(prompt)    
    
    except Exception as e:
        return f"Error analyzing code: {e}"

def generate_doc_for_code(file_path):
    """
    Generate documentation for the code using OpenAI API and return a quality report.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code_content = file.read()
        prompt = f"""
                    Reverse engineer the following code and provide detailed documentations of the code. The report should be structured in an HTML format with a `<head>` containing metadata and a `<body>` with a title, introduction, Code documentations and the ordered list of recommendations.\n
                    
                    Code:
                    {code_content}
                    \n\n
                    Output format:\n
                    - Provide details documentations of the code.\n
                    - The report should be structured in an HTML format with a `<head>` containing metadata and a `<body>` with a title, introduction, Code documentations and the ordered list of recommendations.\n
                    - Each recommendation in the ordered list should have a brief description followed by the suggested improvement or best practice.\n
                    - Ensure the HTML is properly formatted with appropriate sections, headings, and lists.\n
                    """
        if TECHNOLOGY != "GEMINI":
            print("Using OpenAI")
            set_openai_api_key()
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a code quality analyzer."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['choices'][0]['message']['content']
        else:
            print("Using Gemini")
            return call_gemini(prompt)

    except Exception as e:
        return f"Error generating documentation: {e}"

def save_report(report, file_path):
    """
    Save the report to the specified file path.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as report_file:
            report_file.write(report)
    except Exception as e:
        print(f"Error saving report: {e}")

def process_folder(generate_doc=False):
    """
    Recursively process each file in the folder and generate a quality report.
    """
    try:
        for root, _, files in os.walk(INPUT_FOLDER):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith(('.py', '.js', '.tsx', '.java', '.cpp', '.html', '.css')):  # Add other extensions as needed
                    print(f"Analyzing: {file_path}")
                    if generate_doc:
                        report = generate_doc_for_code(file_path)
                    else:
                        report = analyze_code(file_path)
                    
                    # Save the report
                    relative_path = os.path.relpath(file_path, INPUT_FOLDER)
                    report_file_path = os.path.join(OUTPUT_FOLDER, relative_path + ".report.html")
                    save_report(report, report_file_path)
    except Exception as e:
        print(f"Error processing folder: {e}")
