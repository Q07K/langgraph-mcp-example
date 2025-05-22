import io
import sys

from openai import OpenAI

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="test",
)

response = client.chat.completions.create(
    model="./Qwen/Qwen3-4B",
    messages=[
        # {"role": "system", "content": "/no_think"},
        {"role": "user", "content": "안녕하세요."},
    ],
    stream=True,
)

for chunk in response:
    content = chunk.choices[0].delta.content
    if content is not None:
        print(content, end="", flush=True)
