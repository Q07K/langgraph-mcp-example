import os

from dotenv import load_dotenv
from huggingface_hub import login, snapshot_download

load_dotenv()

login(token=os.getenv("HUGGINGFACE_TOKEN"))

repo_id = "Qwen/Qwen3-4B"
model_path = snapshot_download(
    repo_id=repo_id, local_dir="llm/" + repo_id + "/"
)
print(f"Model downloaded to {model_path}")
