import os
from flask import request, jsonify
from secretes.secrets import OPENAI_API_KEY
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import ChatMessage

# Set the OpenAI API key as an environment variable
try:
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
except Exception as e:
    print(f"Error setting environment variable: {e}")

# Define the tool to validate the input code
def validate_input_code(code):
    # Prompt for the validation
    prompt = f"""
    Validate the following code for best practices, correctness, and security:
    
    {code}
    
    Provide detailed feedback and recommendations in an ordered list one by one.
    """
    print("Prompt for validation created.")
    chat_model = ChatOpenAI(model=os.environ.get("X-Ai-Model", "gpt-4"), temperature=0.7)
    print("Chat model initialized.")
    response = chat_model([ChatMessage(content=prompt, role="user")])
    print("Response received from chat model.")
    return response

# Define LangChain Tool
validate_code_tool = Tool(
    name="code_validator_tool",
    func=validate_input_code,
    description="Validates and provides recommendations for input code.",
    handle_parsing_errors=True,
)

# Initialize the agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
tools = [validate_code_tool]
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)

# Endpoint to validate code
def validate_code():
    if 'code' not in request.form:
        return jsonify({"error": "No code provided"}), 400

    input_code = request.form['code']
    if not input_code:
        return jsonify({"error": "No code provided"}), 400

    print("Running agent with input code.")
    response = agent.run(input_code)
    print("Agent run completed.")
    return jsonify({"validation_result": response})

# Function to add the validation endpoint to the Flask app
def render_ai_agent(app):
    app.add_url_rule('/validate-code', 'validate_code_api', validate_code, methods=['POST'])
    return app
