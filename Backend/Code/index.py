from flask import request, jsonify, send_file
import os
import zipfile
import logging
from .gitClone import clone_github_repo
from .codeReview import process_folder

report_path = './Code/report'
src_code_path = './Code/src_code'
zip_path = './Code/repo.zip'

logging.basicConfig(level=logging.INFO)

def clear_folder(dest_folder):
    """
    Clear all files and directories in the specified folder.
    """
    if not os.path.exists(dest_folder):
        return

    for root, dirs, files in os.walk(dest_folder, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            remove_file(file_path)
        for name in dirs:
            dir_path = os.path.join(root, name)
            remove_dir(dir_path)

def remove_file(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        logging.error(f"Error removing file {file_path}: {e}")

def remove_dir(dir_path):
    try:
        os.rmdir(dir_path)
    except OSError as e:
        logging.error(f"Error removing directory {dir_path}: {e}")

def submit_repo():
    try:
        data = request.get_json()
        git_repo_link = data.get('git_repo_link')
        
        clear_folder(src_code_path)
        clear_folder(report_path)

        if not git_repo_link:
            return jsonify({'error': 'git_repo_link is required'}), 400
        
        result = clone_github_repo(git_repo_link)
        return jsonify({'result': result}), 200
    except KeyError as e:
        logging.error(f"KeyError: {e}")
        return jsonify({'error': 'Invalid input data'}), 400
    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({'error': str(e)}), 500

def process_code():
    try:
        process_folder()
        clear_folder(src_code_path)
        
        html_files = [f for f in os.listdir(report_path) if f.endswith('.html')]
        
        if not html_files:
            return jsonify({'error': 'No HTML files found in the reports folder'}), 404
        
        html_file_path = os.path.join(report_path, html_files[0])
        return send_file(html_file_path, as_attachment=True)
    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError: {e}")
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({'error': str(e)}), 500

def generate_doc_for_code_fn():
    try:
        data = process_folder(generate_doc=True)
        clear_folder(src_code_path)
        
        html_files = [f for f in os.listdir(report_path) if f.endswith('.html')]
        
        if not html_files:
            return jsonify({'error': 'No HTML files found in the reports folder'}), 404
        
        html_file_path = os.path.join(report_path, html_files[0])
        return send_file(html_file_path, as_attachment=True)
    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError: {e}")
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({'error': str(e)}), 500

def create_zip_of_repo(repo_path, zip_path):
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(repo_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        zipf.write(file_path, os.path.relpath(file_path, repo_path))
                    except OSError as e:
                        logging.error(f"Error adding file to zip {file_path}: {e}")
                        raise
    except Exception as e:
        logging.error(f"Exception: {e}")
        raise Exception(f"Error creating zip file: {str(e)}")

def download_repo():
    try:
        create_zip_of_repo(report_path, zip_path)
        clear_folder(report_path)
        return send_file(zip_path, as_attachment=True)
    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError: {e}")
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logging.error(f"Exception: {e}")
        return jsonify({'error': str(e)}), 500

def render_code_review_agent(app):
    app.add_url_rule('/submit-repo', 'submit_repo_api', submit_repo, methods=['POST'])
    app.add_url_rule('/process-code', 'process_folder_api', process_code, methods=['GET'])
    app.add_url_rule('/generate-doc', 'generate_doc_for_code_api', generate_doc_for_code_fn, methods=['GET'])
    app.add_url_rule('/download-repo', 'download_repo_api', download_repo, methods=['GET'])
    return app
