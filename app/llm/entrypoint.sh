#!/bin/bash
set -e

API_KEY="$api_key"
DTYPE="$dtype"
MAX_NUM_SEQS="$max_num_seqs"
MAX_MODEL_LEN="$max_model_len"

exec /root/.local/bin/uv run vllm serve \
    "./Qwen/Qwen3-4B" \
    --host "0.0.0.0" \
    --port "8000"\
    --gpu-memory-utilization "0.95"\
    --api-key "$API_KEY"\
    --dtype "$DTYPE"\
    --max-num-seqs "$MAX_NUM_SEQS"\
    --max-model-len "$MAX_MODEL_LEN"
    "$@"
