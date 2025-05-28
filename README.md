# langgraph-mcp-example

## 1. 기본 설정
.env
```text

``` 

## 2. LLM 설치 및 실행

### LLM 설치
```shell
uv run ./app/llm/save_llm.py
```

### Docker build
```shell
cd app/llm
docker build -t qwen3-4b:v1.0.0 .
```

### Docker run
```shell
docker run --gpus all -it -p 8000:8000 -e api_key="..." -e dtype="auto" -e max_num_seqs="1" -e max_model_len="32k" qwen3-4b:v1.0.0
```


# Local test

## 실행 환경 정보
- **CPU:** Intel(R) Core(TM) i5-10400F CPU @ 2.90GHz
- **RAM:** 32GB
- **GPU:** NVIDIA GeForce RTX 2060 12GB
- **Nvidia Driver Version:** 561.09
- **CUDA Version:** 12.6

## Docker run
```shell
docker run --gpus all -it -p 8000:8000 -e api_key="test" -e dtype="float16" -e max_num_seqs="1" -e max_model_len="10k" qwen3-4b:v1.0.0
```
```shell
# INFO 05-21 18:17:01 [model_runner.py:1146] Model loading took 7.5552 GiB and 30.643008 seconds
# INFO 05-21 18:17:06 [worker.py:267] Memory profiling takes 5.29 seconds
# INFO 05-21 18:17:06 [worker.py:267] the current vLLM instance can use total_gpu_memory (12.00GiB) x gpu_memory_utilization (0.95) = 11.40GiB
# INFO 05-21 18:17:06 [worker.py:267] model weights take 7.56GiB; non_torch_memory takes 0.04GiB; PyTorch activation peak memory takes 0.74GiB; the rest of the memory reserved for KV Cache is 3.06GiB.
# INFO 05-21 18:17:06 [executor_base.py:112] # cuda blocks: 1394, # CPU blocks: 1820
# INFO 05-21 18:17:06 [executor_base.py:117] Maximum concurrency for 10000 tokens per request: 2.23x
```

## 실행 테스트
```python
import time
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="test",
)

response = client.chat.completions.create(
    model="./Qwen/Qwen3-4B",
    messages=[
        {"role": "system", "content": "너는 어떤 질문에도 정답을 말해야해"},
        {"role": "user", "content": "hi"},
    ],
    stream=True,
)

for chunk in response:
    content = chunk.choices[0].delta.content
    if content is not None:
        print(content, end="", flush=True)
        
```