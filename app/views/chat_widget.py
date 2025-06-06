import streamlit as st
from langgraph.graph.graph import CompiledGraph

from app.models import chat_model
from app.services.mcp_client import astream_agent


def view_messages(messages: list[dict]) -> None:
    with st.container():
        for message in messages:
            with st.chat_message(message.get("role")):
                st.markdown(message.get("content"))


def chat_input() -> dict | None:
    user_input = st.chat_input()
    if user_input is not None:
        return chat_model.user_message(content=user_input)
    return None


async def ai_message(agent: CompiledGraph, messages: list[dict[str, str]]):
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
