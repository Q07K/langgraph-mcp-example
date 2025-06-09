"""chat model"""


def user_message(content: str) -> dict[str, str]:
    """User Message를 나타내는 딕셔너리 생성

    Parameters
    ----------
    content : str
        메시지 내용

    Returns
    -------
    dict[str, str]
        주어진 내용을 포함하는 딕셔너리
    """
    return {
        "role": "user",
        "content": content,
    }


def system_message(content: str) -> dict[str, str]:
    """System Message를 나타내는 딕셔너리 생성

    Parameters
    ----------
    content : str
        메시지 내용

    Returns
    -------
    dict[str, str]
        주어진 내용을 포함하는 딕셔너리
    """
    return {
        "role": "system",
        "content": content,
    }


def assistant_message(content: str) -> dict[str, str]:
    """Assistant Message를 나타내는 딕셔너리 생성

    Parameters
    ----------
    content : str
        메시지 내용

    Returns
    -------
    dict[str, str]
        주어진 내용을 포함하는 딕셔너리
    """
    return {
        "role": "assistant",
        "content": content,
    }
