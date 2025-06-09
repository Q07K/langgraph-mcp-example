from typing import AsyncGenerator

import streamlit as st
from langgraph.graph.graph import CompiledGraph

from app.models import chat_model
from app.services.mcp_client import astream_agent


def reset_history() -> None:
    """Streamlit 세션 상태의 채팅 기록을 초기화합니다.

    이 함수는 `st.session_state`에 저장된 'messages' 키의 값을
    빈 리스트(`[]`)로 재설정하여, 현재까지의 모든 대화 기록을 삭제합니다.
    'Chat Reset'버튼의 콜백 함수로 사용됩니다.

    Returns
    -------
    None
        이 함수는 None을 반환합니다.
    """
    st.session_state["messages"] = []


def view_messages(messages: list[dict]) -> None:
    """채팅 기록을 화면에 표시(랜더링)합니다.

    이 함수는 메시지 딕셔너리 리스트를 순회하며, 각 메시지의 'role'과
    'content'를 사용하여 Streamlit의 `st.chat_message` 컨테이너 내에
    채팅 내용을 렌더링합니다.

    Parameters
    ----------
    messages : list[dict]
        화면에 표시할 메시지 딕셔너리의 리스트.
        각 딕셔너리는 반드시 'role' (str)과 'content' (str) 키를 포함해야 합니다.
    """
    with st.container():
        for message in messages:
            with st.chat_message(message.get("role")):
                st.markdown(message.get("content"))


def chat_input() -> dict | None:
    """Streamlit 채팅 입력 위젯에서 사용자 입력을 받아 처리합니다.

    이 함수는 `st.chat_input`을 사용하여 사용자로부터 텍스트 입력을 기다립니다.
    사용자가 메시지를 입력하고 제출하면, 해당 내용을 `chat_model.user_message`
    메서드로 감싸 딕셔너리 형태로 반환합니다. 입력이 없을 경우 `None`을 반환합니다.

    Returns
    -------
    dict | None
        메시지를 입력한 경우, 'role'과 'content' 키를 포함하는 딕셔너리를 반환합니다.
        입력이 없을 경우 None을 반환합니다.
    """
    user_input = st.chat_input()
    if user_input is not None:
        return chat_model.user_message(content=user_input)
    return None


async def ai_message(
    agent: CompiledGraph,
    messages: list[dict[str, str]],
) -> AsyncGenerator[str, None, None]:
    """AI 에이전트의 응답을 스트리밍하고 UI에 진행 상황을 표시합니다.

    이 함수는 비동기 제너레이터로 AI 에이전트(`astream_agent`)를 호출하여
    응담을 실시간으로 스트리밍합니다.
    에이전트가 도구(tool)을 사용하는 중간 과정을 만나면 Streamlit `popover`에
    해당 정보를 표시하고, 최종적인 텍스트 응답(content)울 렌더링합니다.
    이후 응답이 완료되면 전체 최종 답변 내용을 세션 상태(`st.session_state`)에
    저장합니다.

    Parameters
    ----------
    agent : CompiledGraph
        LangGraph로 컴파일된 ReAct AI 에이전트입니다.
    messages : list[dict[str, str]]
        에이전트에게 전달할 대화 기록. 각 메시지는 'role'과 'content'를
        포함하는 딕셔너리입니다.

    Yields
    ------
    AsyncGenerator[str, None]
        AI 에이전트의 각 노드가 생성하는 응답 텍스트의 스트리밍 청크(chunk)
    """
    async for message in astream_agent(
        agent=agent,
        messages=messages,
    ):
        if message.type == "tool":
            with st.popover(f"🛠️: {message.name}"):
                st.json(message)
    else:
        content = message.content
        yield content
        st.session_state["messages"].append(
            chat_model.assistant_message(content=content)
        )
