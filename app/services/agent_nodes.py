import json
from typing import Callable

from langchain_core.messages import AIMessage
from langchain_core.messages.base import BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessagesState

from app.utils.agent_utils import repair_json_string


def call_model_node(
    model: ChatOpenAI,
) -> Callable[..., dict[str, list[BaseMessage]]]:
    """`ChatOpenAI` 모델을 사용하여 메시지 상태를 처리하는 함수(callable)를 반환합니다.

    LangGraph Node에 사용될 함수로 `ChatOpenAI` 모델을 넘겨주기 위해 구성된 함수입니다.

    Parameters
    ----------
    model : ChatOpenAI
        메시지를 처리할 OpenAI 챗 모델 인스턴스.

    Returns
    -------
    Callable[..., dict[str, list[BaseMessage]]]
        `call_model` 함수.
    """

    def call_model(state: MessagesState) -> dict[str, list[BaseMessage]]:
        """현재 메시지 상태를 바탕으로 모델을 호출하고 응답 메시지를 반환합니다.


        Parameters
        ----------
        state : MessagesState
            현재 대화 상태를 담고 있는 메시지 목록.

        Returns
        -------
        dict[str, list[BaseMessage]]
            모델 응답이 포함된 새 메시지 상태.
        """
        mesages = state["messages"]
        response = model.invoke(mesages)
        return {"messages": [response]}

    return call_model


def check_tool_usage_node(state: MessagesState) -> str:
    """마지막 AI 메시지에 도구 호출(tool_calls)이 포함되어 있는지 확인합니다.

    Parameters
    ----------
    state : MessagesState
        현재 대화 상태를 담고 있는 메시지 목록.

    Returns
    -------
    str
        도구 호출이 있으면 'json_repair', 없으면 '__end__'를 반환합니다.
    """
    messages = state["messages"]
    last_message: AIMessage = messages[-1]
    if last_message.tool_calls:
        return "json_repair"
    return END


def json_repair_node(
    state: MessagesState,
) -> dict[
    str,
    list[BaseMessage],
]:
    """마지막 AI 메시지에 포함된 도구 호출의 JSON 인자를 복구합니다.

    Parameters
    ----------
    state : MessagesState
        현재 대화 상태를 담고 있는 메시지 목록.

    Returns
    -------
    dict[str, list[BaseMessage]]
        복구된 도구 호출을 포함하는 새 메시지 목록을 반환합니다.
    """
    messages = state["messages"]
    last_message: AIMessage = messages[-1]

    repaired_tool_calls = []

    for tool_call in last_message.additional_kwargs.get("tool_calls", []):
        args_str = tool_call["function"]["arguments"]
        repaired_args_str = repair_json_string(args_str)

        try:
            repaired_args = json.loads(repaired_args_str)
            repaired_tool_calls.append(
                {
                    "id": tool_call["id"],
                    "name": tool_call["function"]["name"],
                    "args": repaired_args,
                }
            )
        except json.JSONDecodeError as e:
            print(f"JSON 복구 후에도 파싱에 실패했습니다: {e}")
            continue

    new_message = AIMessage(
        content=last_message.content,
        tool_calls=repaired_tool_calls,
        id=last_message.id,  # 원본 ID 등을 유지하여 추적성을 높입니다.
    )
    return {"messages": messages[:-1] + [new_message]}
