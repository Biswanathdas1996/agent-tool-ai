from flask import Flask, request
import os
from Mongodb.rag import render_mongo_pack
from Mongodb.data_handling import render_mongo_data_pack
from AI_agents.app import render_ai_agent
from Devops.index import render_deploy_agent
from Code.index import render_code_review_agent
from Gpt.index import render_gpt_pack
from Azure_Cosmos.index import render_cosmos_pack
from img_to_html.index import render_img_to_html_pack
from CodeCompare.index import render_code_compare_pack
from DataGenerator.index import render_data_generator
from secretes.secrets import OPENAI_API_KEY
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from TestScriptCustom.index import render_html_extract_elements


def create_app():
    """
    Create and configure the Flask application.
    
    Modules and Packages:
    - render_mongo_pack: Integrates MongoDB related functionalities.
    - render_mongo_data_pack: Integrates MongoDB data handling functionalities.
    - render_ai_agent: Integrates AI agent functionalities.
    - render_deploy_agent: Integrates deployment agent functionalities.
    - render_code_review_agent: Integrates code review agent functionalities.
    - render_gpt_pack: Integrates GPT related functionalities.
    Environment Variables:
    - IMG_UPLOAD_FOLDER: Directory for image uploads.
    - OPENAI_API_KEY: API key for OpenAI services.
    - X-Ai-Model: Custom header for AI model selection.
    """
    app = Flask(__name__)
    # CSRFProtect(app)
    CORS(app)
    # app.config['WTF_CSRF_ENABLED'] = False  # Enable CSRF protection
    
    try:
        app = render_mongo_pack(app)
        # app = render_cosmos_pack(app)
        app = render_mongo_data_pack(app)
        app = render_ai_agent(app)
        app = render_deploy_agent(app)
        app = render_code_review_agent(app)
        app = render_gpt_pack(app)
        app = render_img_to_html_pack(app)
        app = render_code_compare_pack(app)
        app = render_data_generator(app)
        app = render_html_extract_elements(app)
    except Exception as e:
        app.logger.error(f"Error initializing modules: {e}")
        raise



    os.environ["IMG_UPLOAD_FOLDER"] = 'Gpt/uploads'
    os.makedirs(os.environ["IMG_UPLOAD_FOLDER"], exist_ok=True)
    
    try:
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    except Exception as e:
        app.logger.error(f"Error setting environment variable: {e}")
        raise

    @app.before_request
    def before_request():
        custom_header = request.headers.get('X-Ai-Model')
        if custom_header:
            os.environ["X-Ai-Model"] = custom_header
            app.logger.info(f"X-Ai-Model header received: {custom_header}")

    

    return app

if __name__ == "__main__":
    try:
        app = create_app()
        app.run(debug=True)
    except Exception as e:
        print(f"Failed to start the application: {e}")