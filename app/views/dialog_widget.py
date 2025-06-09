"""Streamlit dialog widget"""

import streamlit as st

from app.utils.mcp_utils import save_mcp_server


@st.dialog(title="Add MCP Server")
def add_mcp_server() -> None:
    """새로운 MCP Server 구성 추가를 위한 다이얼로그를 표시합니다.

    Streamlit `@st.dialog`를 사용하여 모달 창을 생성합니다.
    다이얼로그 안에는 텍스트 입력을 위한 폼(form)이 있으며, 'Add' 버튼을 누르면
    입력된 내용이 `save_mcp_server` 함수를 호출하여 입력을 저장합니다.
    이후 `st.rerun()`으로 앱을 새로고침합니다.
    """
    with st.form(key="Add", border=False):
        str_input = st.text_area(
            label="Add MCP Server",
            height=400,
            label_visibility="collapsed",
        )
        if st.form_submit_button(label="Add", use_container_width=True):
            save_mcp_server(str_input=str_input)
            st.rerun()
