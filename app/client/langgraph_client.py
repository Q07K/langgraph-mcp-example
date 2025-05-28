import asyncio

from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

BASE_URL = "http://localhost:8000/v1"
API_KEY = "test"

model = ChatOpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
    model="./Qwen/Qwen3-4B",
)

server_params = StdioServerParameters(
    command="python",  # 실행할 명령
    args=["math_server.py"],  # 인자(스크립트 경로)
    # cwd=..., env=... # 선택적 작업 디렉터리 및 환경 변수
)


async def main():

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            print("세션 초기화 중...")
            # 서버와 핸드 셰이크 수행
            await session.initialize()
            print("세션이 초기화되었습니다.")

            print("MCP 도구 로드 중...")
            # MCP 도구를 가져오고 LangChain 도구로 변환
            tools = await load_mcp_tools(session)
            print(f"로드된 도구: {[tool.name for tool in tools]}")

            # 모델과 로드된 도구를 사용하여 LangGraph ReAct 에이전트 생성
            agent = create_react_agent(model, tools)

            print("에이전트 호출 중...")
            # 에이전트 실행

            result = await agent.ainvoke({"messages": "what's (3 + 5) * 12?"})
            print(result)

            # 또는 최종 응답을 직접 얻을 수 있습니다
            # final_response = await agent.ainvoke(inputs)
            # print("에이전트 응답:", final_response['messages'][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
