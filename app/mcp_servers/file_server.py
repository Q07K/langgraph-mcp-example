"""MCP Server file"""

import os

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="FileManager")


@mcp.tool()
def list_files(directory: str = ".", limit: int = 10) -> str:
    """디렉토리의 파일 목록을 가져옵니다

    Parameters
    ----------
    directory : str, optional
        조회할 디렉토리 경로, by default "."
    limit : int, optional
        조회할 디렉토리 내부 파일 겟수, by default 10

    Returns
    -------
    str
        파일 목록 문자열
    """

    try:
        files = os.listdir(directory)

        file_list = "\n".join(files[:limit])

        return f"{directory} 디렉토리 파일 목록:\n{file_list}"
    except Exception as e:
        return f"오류: {e}"


@mcp.tool()
def file_info(filename: str) -> str:
    """파일 정보를 가져옵니다

    Parameters
    ----------
    filename : str
        정보를 확인할 파일명

    Returns
    -------
    str
        파일 정보 문자열
    """
    if os.path.exists(filename):
        size = os.path.getsize(filename)
        return f"{filename}: 크기 {size} bytes"

    return f"{filename}: 파일이 존재하지 않습니다."


if __name__ == "__main__":
    # stdio 전송을 사용하여 서버 실행
    print("Starting Math MCP server via stdio...")
    mcp.run(transport="stdio")
