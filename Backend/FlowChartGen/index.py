

from google import genai
from pydantic import BaseModel
from flask import Flask, request, jsonify
import json
GEMINI_API_KEY = "AIzaSyB6SXZ8k-Otk4NmfFvXK6lzqqRCScksku4"

class Node(BaseModel):
    id: str
    type: str
    data: dict = {"key": "value"}  # Define a schema for data with example properties
    position: dict = {"x": 0, "y": 0}  # Define a schema for position with example properties

class Edge(BaseModel):
    id: str
    source: str
    target: str

class Flowchart(BaseModel):
    nodes: list[Node]
    edges: list[Edge]



sample_output = {
        "nodes": [
            {
                "id": "{start_node_id}",
                "type": "input",
                "data": {"label": "{start_label}"},
                "position": {"x": 0, "y": 0}
            },
            {
                "id": "{step1_node_id}",
                "data": {"label": "{step1_label}"},
                "position": {"x": 100, "y": 100}
            },
            {
                "id": "{end_node_id}",
                "data": {"label": "{end_label}"},
                "position": {"x": 200, "y": 200}
            }
        ],
        "edges": [
            {
                "id": "e{start_node_id}-{step1_node_id}",
                "source": "{start_node_id}",
                "target": "{step1_node_id}"
            },
            {
                "id": "e{step1_node_id}-{end_node_id}",
                "source": "{step1_node_id}",
                "target": "{end_node_id}"
            }
        ]
    }

def generate_flowchart_description(api_key, model_name, flowchart_title, flowchart_description, sample_output):
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_name,
        contents=f"""The flowchart titled "{flowchart_title}" is designed to {flowchart_description}.
        
        Sample output: 
        {sample_output}
        """,
        config={
            'response_mime_type': 'application/json'
        },
    )
    return json.loads(response.text)


def generate_flowchart():
    data = request.get_json()
    flowchart_title = data.get('title', 'Untitled Flowchart')
    flowchart_description = data.get('description', '')
    
    response_text = generate_flowchart_description(
        api_key=GEMINI_API_KEY,
        model_name='gemini-2.0-flash',
        flowchart_title=flowchart_title,
        flowchart_description=flowchart_description,
        sample_output=sample_output
    )
    
    return jsonify(response_text)


def render_flow_diagram_gen(app):
    app.add_url_rule('/generate-flowchart', 'generate_flowchart_api', generate_flowchart, methods=['POST'])
    return app 
