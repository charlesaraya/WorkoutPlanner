import json

def parse_response(response):
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed. Raw response: {response.content}")
        raise ValueError(f"Invalid JSON from LLM: {e}")
    return result