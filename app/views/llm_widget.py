import streamlit as st

LLM_LIST = [
    "./Qwen/Qwen2.5-7B-Instruct",
    # "./Qwen/Qwen3-4B",
    "./Qwen/Qwen3-8B",
]


def view_llm_list():
    st.markdown("**Select Model**")
    st.selectbox(
        label="LLM",
        options=LLM_LIST,
        key="selected_llm",
        index=0,
        label_visibility="collapsed",
    )


def base_url_input():
    st.markdown("**Base URL**")
    st.text_input(
        label="Base URL",
        key="base_url",
        value="http://localhost:8000/v1",
        label_visibility="collapsed",
    )


def api_key_input():
    st.markdown("**API KEY**")
    st.text_input(
        label="API KEY",
        key="api_key",
        type="password",
        label_visibility="collapsed",
    )
