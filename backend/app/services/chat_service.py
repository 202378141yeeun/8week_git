from backend.app.ai.llm_client import generate_reply


def chat_reply(message: str) -> str:
    """챗봇 비즈니스 로직 레이어.

    나중에 로그 저장, 사용량 카운트, 검열 로직 등을
    이 함수에 붙이면 된다.
    """
    return generate_reply(message)
