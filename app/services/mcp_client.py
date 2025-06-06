from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent


async def connect_client(
    model: str,
    base_url: str,
    api_key: str,
    mcp_server_config: dict,
):
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


async def astream_agent(agent: CompiledGraph, messages: list[dict[str, str]]):
    async for chunk in agent.astream(
        input={"messages": messages},
        stream_mode="values",
    ):
        message = chunk["messages"][-1]
        if message.type in ["ai", "tool"]:
            yield message
