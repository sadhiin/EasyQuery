import re

# cleanup the ``` from the ai response

def clean_ai_response(response: str) -> str:
    # Remove any leading/trailing whitespace and newlines
    response = response.strip()
    # Remove code block markers
    response = re.sub(r"```.*?```", "", response, flags=re.DOTALL)
    return response