# langgraph-mcp-example

## 1. 기본 설정

### `.env` 파일 생성
```text
HUGGINGFACE_TOKEN = "허깅페이스 API KEY 입력"
API_KEY = "vLLM에서 사용할 API KEY 입력"
MODELS = "./Qwen/Qwen3-4B, "  # 사용 할 모델 목록을 ", "를 기준으로 추가 가능
```


## 2. LLM 설치 및 실행

### LLM 설치
```shell
uv run ./llm/save_llm.py
```

### Docker build
```shell
cd ./llm
docker build -t qwen3-4b:v1.0.0 .
```

### Docker run
```shell
docker run --gpus all -it -p 8000:8000 -e api_key="..." -e dtype="auto" -e max_num_seqs="1" -e max_model_len="32k" qwen3-4b:v1.0.0
```

## 3. Streamlit 실행
### 가상환경 활성화
**windows**
```shell
.\.venv\Scripts\activate
```

**Linux**
```shell
source .\.venv\bin\activate
```

### strteamlit 실행
```shell
streamlit run ./main.py
```

# Local Run

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
```shell
uv run ./run_llm.py
```

## streamlit 실행
```shell
streamlit run ./main.py
```