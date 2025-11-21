from typing import Optional

from langchain_openai import ChatOpenAI

from backend.app.config.settings import settings


_llm: Optional[ChatOpenAI] = None

if settings.OPENAI_API_KEY:
    _llm = ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        model=settings.OPENAI_MODEL,
        temperature=0.2,
    )


def generate_reply(message: str) -> str:
    """사용자 메시지를 받아 AI 응답을 생성한다.

    OPENAI_API_KEY가 없으면 데모용 에코 응답을 돌려준다.
    """
    if _llm is None:
        return f"(데모 모드) 당신이 보낸 메시지: {message}"

    resp = _llm.invoke(message)
    return resp.content
