import io
import sys

from openai import OpenAI

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="test",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current temperature for a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and country e.g. Bogotá, Colombia",
                    }
                },
                "required": ["location"],
                "additionalProperties": False,
            },
        },
    }
]

response = client.chat.completions.create(
    model="./Qwen/Qwen3-4B",
    messages=[
        {"role": "user", "content": "오늘 서울 날씨가 어떄?"},
    ],
    tools=tools,
    tool_choice="auto",
)
print(response)
