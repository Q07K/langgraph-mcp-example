"""MCP Client"""

from typing import AsyncGenerator

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent


async def connect_client(
    model: str,
    base_url: str,
    api_key: str,
    mcp_server_config: dict,
) -> CompiledGraph:
    """LLM과 MCP 도구를 결합한 LangGraph 에이전트를 생성합니다.

    전달받은 인증 정보로 `ChatOpenAI` 모델을 초기화하고, MCP Server 설정으로
    `MultiServerMCPClient`를 생성합니다. 클라이언트에서 사용 가능한 도구(tools)를
    가져온 뒤, 모델과 도구를 `create_react_agent` 함수에 전달하여 최종적으로
    실행 가능한 대화형 에이전트를 구성하고 반환합니다.

    Parameters
    ----------
    model : str
        사용할 LLM 모델의 이름.
    base_url : str
        LLM API의 Base URL.
    api_key : str
        LLM API 인증을 위한 API KEY.
    mcp_server_config : dict
        `MultiServerMCPClient`에 전달될 MCP Server 연결 정보.

    Returns
    -------
    CompiledGraph
        LLM과 MCP 도구가 결합된, 실행 준비가 완료된 LangGraph 에이전트.
    """
    model = ChatOpenAI(
        model=model,
        base_url=base_url,
        api_key=api_key,
        temperature=0.4,
    )

    client = MultiServerMCPClient(connections=mcp_server_config)
    tools = await client.get_tools()

    agent = create_react_agent(model, tools)
    return agent


async def astream_agent(
    agent: CompiledGraph, messages: list[dict[str, str]]
) -> AsyncGenerator[str, None]:
    """LangGraph 에이전트의 응답을 비동기 스트림으로 반환합니다.

    주어진 에이전트와 채팅 기록을 사용하여 `agent.astream` 메서드를 호출합니다.
    에이전트가 실행되며 생성하는 각 단계(chunk) 중, AI 응답("ai") 또는
    도구 호출("tool")에 해당하는 최종 메시지만을 필터링하여 `yield`합니다.

    Parameters
    ----------
    agent : CompiledGraph
        `connect_client`를 통해 생성된, 실행 가능한 LangGraph 에이전트.
    messages : list[dict[str, str]]
        에이전트에게 전달할 채팅 기록.

    Yields
    ------
    Any
        AI 응답 또는 도구 호출을 나타내는 메시지 객체(Message).
    """
    async for chunk in agent.astream(
        input={"messages": messages},
        stream_mode="values",
    ):
        message = chunk["messages"][-1]
        if message.type in ["ai", "tool"]:
            yield message
