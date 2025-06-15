"""LangGarph Agent"""

from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessagesState, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode

from app.services import agent_nodes


def custom_create_react_agent(
    model: ChatOpenAI,
    tools: list[BaseTool],
) -> CompiledStateGraph:
    """도구 사용 및 JSON 복구 로직이 포함된 LangGraph 기반 ReAct 에이전트를 생성합니다.

    LLM이 도구를 사용할 수 있도록 구성된 LangGraph 상태 기반 워크플로우(StateGraph)를
    빌드하고 컴파일합니다. 모델이 생성한 응답이 JSON 형식 오류를 포함하는 경우 이를
    복구한 뒤 도구를 사용하는 흐름을 반복하며, 최종적으로 종료 상태에 도달합니다.
    Parameters
    ----------
    model : ChatOpenAI
        언어 에이전트로 사용될 ChatOpenAI 모델 인스턴스입니다.
    tools : list[BaseTool]
        모델과 ToolNode에 연결될 도구 목록입니다.
        각 도구는 MCP Servers 에서 제공되는 목록입니다.

    Returns
    -------
    CompiledStateGraph
        실행 가능한 형태로 컴파일된 LangGraph 상태 기반 워크플로우(StateGraph)입니다.
    """
    model = model.bind_tools(tools=tools)

    tool_node = ToolNode(tools=tools)

    # Build graph
    builder = StateGraph(state_schema=MessagesState)
    builder.add_node(
        node="agent",
        action=agent_nodes.call_model_node(model=model),
    )
    builder.add_node(node="json_repair", action=agent_nodes.json_repair_node)
    builder.add_node(node="tools", action=tool_node)

    # Logic
    builder.add_edge(start_key=START, end_key="agent")
    builder.add_conditional_edges(
        source="agent",
        path=agent_nodes.check_tool_usage_node,
        path_map=["json_repair", END],
    )
    builder.add_edge(start_key="json_repair", end_key="tools")
    builder.add_edge(start_key="tools", end_key="agent")

    # Compile
    agent = builder.compile()

    return agent
