# math_server.py
from mcp.server.fastmcp import FastMCP

# 이름으로 MCP 서버 초기화
mcp = FastMCP(
    "Math",  # Name of the MCP server
    instructions="You are a Math assistant that can provide the current Math",  # Instructions for the LLM on how to use this tool
    host="0.0.0.0",  # Host address (0.0.0.0 allows connections from any IP)
    port=8005,  # Port number for the server
)


@mcp.tool()
def add(a: int, b: int) -> int:
    """두 숫자를 더합니다"""
    return a + b


@mcp.tool()
def subtraction(a: int, b: int) -> int:
    """두 숫자를 뺍니다"""
    return a - b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """두 숫자를 곱합니다"""
    return a * b


@mcp.tool()
def divide(a: int, b: int) -> float:
    """두 숫자를 나눕니다"""
    return a / b


# 예제 프롬프트 정의
@mcp.prompt()
def configure_assistant(skills: str) -> list[dict]:
    """지정된 기술로 어시스턴트를 구성합니다."""
    return [
        {
            "role": "assistant",  # AIMessage에 해당합니다
            "content": f"당신은 유용한 어시스턴트입니다. 다음 기술을 보유하고 있습니다: {skills}. 항상 한 번에 하나의 도구만 사용하세요.",
        }
    ]


if __name__ == "__main__":
    # stdio 전송을 사용하여 서버 실행
    print("Starting Math MCP server via stdio...")
    mcp.run(transport="sse")
