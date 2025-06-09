"""Streamlit sidebar widget"""

import streamlit as st

from app.utils.mcp_utils import set_mcp_server
from app.views import llm_widget, mcp_widget
from app.views.chat_widget import reset_history
from app.views.dialog_widget import add_mcp_server


def sidebar() -> None:
    """Streamlit 애플리케이션의 사이드바 UI를 구성하고 표시합니다.

    사이드바에 표시될 모든 UI 요소를 구성하는 역할을 합니다.
    LLM 모델 선택, Base URL 및 API 키 입력 필드를 포함하는 'LLM' 섹션과
    MCP 서버 목록을 표시하고 관리하는 'MCP Servers' 섹션으로 구성됩니다.
    또한, MCP 서버를 추가하는 다이얼로그를 열거나 채팅 기록을 초기화하는
    버튼이 구성되어있습니다.

    """
    st.title("LLM")
    llm_widget.view_llm_list()
    llm_widget.base_url_input()
    llm_widget.api_key_input()
    st.divider()

    st.title("MCP Servers")
    server_config = set_mcp_server()
    mcp_widget.view_mcp_servers(
        mcp_servers=server_config,
    )
    st.divider()
    col1, col2 = st.columns(2, gap="large")
    col1.button(
        label="Add",
        use_container_width=True,
        on_click=add_mcp_server,
    )
    col2.button(
        label="Chat Reset",
        use_container_width=True,
        on_click=reset_history,
    )
