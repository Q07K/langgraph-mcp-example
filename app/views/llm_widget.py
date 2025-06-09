"""Streamlit llm widget"""

import os

import streamlit as st

# 사용 가능한 모델 목록을 환경 변수에서 불러옵니다.
MODELS = os.getenv("MODELS", "").split(", ")


def view_llm_list() -> None:
    """LLM 모델을 선택할 수 있는 드롭다운 메뉴를 표시합니다.

    환경 변수(`MODELS`)에서 가져온 모델 목록으로 selectbox를 생성합니다.
    선택된 모델 이름은 `st.session_state.selected_llm`에 저장됩니다.
    """
    st.markdown("**Select Model**")
    st.selectbox(
        label="LLM",
        options=MODELS,
        key="selected_llm",
        index=0,
        label_visibility="collapsed",
    )


def base_url_input() -> None:
    """API의 Base URL을 입력받는 텍스트 필드를 표시합니다.

    기본값으로 'http://localhost:8000/v1'이 설정된 텍스트 입력 필드를
    생성합니다. 입력된 URL 값은 `st.session_state.base_url`에 저장됩니다.
    """
    st.markdown("**Base URL**")
    st.text_input(
        label="Base URL",
        key="base_url",
        value="http://localhost:8000/v1",
        label_visibility="collapsed",
    )


def api_key_input() -> None:
    """API KEY를 입력받는 비밀번호 필드를 표시합니다.

    입력 내용이 가려지는 비밀번호 타입의 텍스트 입력 필드를 생성합니다.
    입력된 API 키 값은 `st.session_state.api_key`에 저장됩니다.
    """
    st.markdown("**API KEY**")
    st.text_input(
        label="API KEY",
        key="api_key",
        type="password",
        label_visibility="collapsed",
    )
