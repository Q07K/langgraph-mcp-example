from json_repair import repair_json
from langchain_openai import ChatOpenAI


def connect_llm(
    model_name: str,
    base_url: str,
    api_key: str,
) -> ChatOpenAI:
    """OpenAI API 호출 방식을 사용하는 모델을 연결합니다.

    Parameters
    ----------
    model_name : str
        사용하고자 하는 LLM 이름.
    base_url : str
        OpenAI API 호출 방식을 사용하는 모델의 Base URL.
    api_key : str
        OpenAI API 호출에 필요한 API KEY.

    Returns
    -------
    ChatOpenAI
        연결된 모델을 반환합니다다.
    """
    return ChatOpenAI(
        model=model_name,
        base_url=base_url,
        api_key=api_key,
        temperature=0.4,
    )


def repair_json_string(json_string: str) -> str:
    """입력 받은`json_string`JSON 문자열을 표준 JSON 문자열로 변환합니다.

    json_repair 라이브러리를 사용해 깨진 JSON 문자열을 복구하고,
    다시 표준 JSON 문자열로 변환합니다.


    Parameters
    ----------
    json_string : str
        JSON 구조를 갖는 문자열.

    Returns
    -------
    str
        복구된 JSON 문자열.
    """
    return repair_json(json_str=json_string, ensure_ascii=False)
