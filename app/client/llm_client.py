import openai

BASE_URI = "http://localhost:8000/v1"
API_KEY = "test"

tools = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Add two numbers together",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        },
    }
]

client = openai.OpenAI(
    base_url=BASE_URI,
    api_key=API_KEY,
)

response = client.chat.completions.create(
    model="./Qwen/Qwen3-4B",
    messages=[
        {"role": "user", "content": "안녕하세요~~"},
    ],
    tools=tools,
)

print(response.choices)
