from Gpt.index import call_gpt
from helper.utils import convert_to_json, convert_string_to_json

SAMPLE_OUTPUT = [
    {
        "x-axis": "field1",
        "y-axis": ["field2"],
        "type": "Bar Chart"
    },
    {
        "x-axis": "field1",
        "y-axis": ["field2", "field3"],
        "type": "Line Chart"
    }
]

def get_analytics(sample_data):
    try:
        print("sample_data", sample_data)
        # Prepare the prompt for OpenAI
        prompt = f"""
            Analyze the following dataset and identify combinations of fields that can be used to create various types of charts. For each combination, provide the following:

            The type of chart (e.g., pie chart, bar chart, line chart).
            Dataset:
            {sample_data}
            Guidelines:
            - The dataset may contain multiple fields.
            - The fields can be used to create different types of charts.
            - The output should include the type of chart and the fields that can be used to create it.
            - The output should be in JSON format.
            - The output should include at least two different combinations of fields and chart types.
            - The output should be based on the dataset provided.
            - only a json data no extra text
            -strict format of the  Output:
            {SAMPLE_OUTPUT}
        """
        # Call GPT to get the converted data
        response = call_gpt("You are a good analytics expert", prompt, 1000)
        return response
    except Exception as e:
        return {"error": str(e)}

def sample_result(result, sample_size=2):
    try:
        return result[:sample_size]
    except Exception as e:
        return {"error": str(e)}

def get_analytics_result(result):
    if isinstance(result, list):
        try:
            sampled_result = sample_result(convert_to_json(result))
            analytics_string = get_analytics(sampled_result)
            analytics = convert_string_to_json(analytics_string)
        except Exception as e:
            analytics = {"error": str(e)}
    else:
        analytics = {}
    return analytics
