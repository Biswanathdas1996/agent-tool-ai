

from google import genai
from pydantic import BaseModel
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

sample= {
  "nodes": [
    {
      "id": "{start_node_id}",
      "type": "input",
      "data": { "label": "{start_label}" },
      "position": { "x": 0, "y": 0 }  # Replace with actual values or variables
    },
    {
      "id": "{step1_node_id}",
      "data": { "label": "{step1_label}" },
      "position": { "x": 100, "y": 100 }  # Replace with actual values or variables
    },
    {
      "id": "{end_node_id}",
      "data": { "label": "{end_label}" },
      "position": { "x": 200, "y": 200 }  # Replace with actual values or variables
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


client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=f"""The flowchart titled "Understanding Flow Charts" is designed to guide users based on their familiarity with flowcharts. 
    It starts by asking whether the user understands flowcharts. If the answer is yes, they are directed to a message saying "Great!"
      and then encouraged to visit the Diagram Community for examples and templates, after which the process ends. If the user does not
        understand flowcharts, they are asked whether they would like to start with the basics. If they agree, they are directed to read a
          complete flowchart guide with examples before reaching the end. If they choose not to start with the basics, they are led to further 
          reading about flowcharts and then reach the end as well. This structured approach ensures that both beginners and experienced users
            are provided with relevant resources to enhance their understanding.
            
            Sample output: 
            {sample}
            
            """,
    config={
        'response_mime_type': 'application/json'
    },
)
# Use the response as a JSON string.
print(response.text)

# # Use instantiated objects.
# my_recipes: list[Flowchart] = response.parsed