import asyncio
import platform

import nest_asyncio
import openai
import streamlit as st
from dotenv import load_dotenv

from app.services.mcp_client import connect_client
from app.views import chat_widget, sidebar_widget

load_dotenv()


# Windows에서 Proactor 이벤트 루프 사용 설정
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# nest_asyncio 적용
nest_asyncio.apply()


def main():
    # 전역 이벤트 루프 생성 및 재사용
    if "event_loop" not in st.session_state:
        loop = asyncio.new_event_loop()
        st.session_state.event_loop = loop
        asyncio.set_event_loop(loop)

    if st.session_state.get("messages") is None:
        st.session_state["messages"] = []
    if st.session_state.get("mcp_servers") is None:
        st.session_state["mcp_servers"] = {}

    with st.sidebar:
        sidebar_widget.sidebar()

    chat_widget.view_messages(messages=st.session_state["messages"])

    user_input = chat_widget.chat_input()
    try:
        if user_input is not None:
            st.session_state["messages"].append(user_input)
            with st.chat_message("user"):
                st.markdown(user_input.get("content"))

            with st.chat_message("ai"):
                st.session_state.event_loop.run_until_complete(generate())
    except openai.OpenAIError as e:
        st.error(e)


async def generate():
    with st.spinner("MCP 서버 연결 중..."):
        agent = await connect_client(
            model_name=st.session_state["selected_llm"],
            base_url=st.session_state["base_url"],
            api_key=st.session_state["api_key"],
            mcp_server_config=st.session_state["mcp_servers"],
        )

    with st.spinner("요청 내용 처리 중..."):
        st.write_stream(
            chat_widget.ai_message(
                agent=agent,
                messages=st.session_state["messages"],
            )
        )


if __name__ == "__main__":
    main()
