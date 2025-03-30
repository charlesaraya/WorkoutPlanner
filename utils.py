import json

def parse_response(content):
    try:
        result = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed. Raw content: {content}")
        raise ValueError(f"Invalid JSON: {e}")
    return result