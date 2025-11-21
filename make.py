# make_dir.py
import os
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    print(f"[DIR] {path}")


def write_file(path: Path, content: str):
    if path.exists():
        print(f"[SKIP] {path} (already exists)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).lstrip("\n"), encoding="utf-8")
    print(f"[FILE] {path}")


def main():
    # ---------------------------
    # 디렉토리 구조 생성
    # ---------------------------
    # backend/app 하위
    backend_app = ROOT / "backend" / "app"
    dirs = [
        backend_app / "api",
        backend_app / "services",
        backend_app / "ai",
        backend_app / "config",
        ROOT / "frontend" / "static",
        ROOT / "frontend" / "templates",
    ]

    for d in dirs:
        ensure_dir(d)

    # ---------------------------
    # __init__.py 기본 파일들
    # ---------------------------
    for pkg in [
        backend_app,
        backend_app / "api",
        backend_app / "services",
        backend_app / "ai",
        backend_app / "config",
    ]:
        write_file(pkg / "__init__.py", "# package init\n")

    # ---------------------------
    # backend/app/config/settings.py
    # ---------------------------
    write_file(
        backend_app / "config" / "settings.py",
        """
        import os


        class Settings:
            \"\"\"기본 설정 모음\"\"\"

            PROJECT_NAME: str = "AI Chat Demo"
            OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
            OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


        settings = Settings()
        """,
    )

    # ---------------------------
    # backend/app/ai/llm_client.py
    # ---------------------------
    write_file(
        backend_app / "ai" / "llm_client.py",
        """
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
            \"\"\"사용자 메시지를 받아 AI 응답을 생성한다.

            OPENAI_API_KEY가 없으면 데모용 에코 응답을 돌려준다.
            \"\"\"
            if _llm is None:
                return f"(데모 모드) 당신이 보낸 메시지: {message}"

            resp = _llm.invoke(message)
            return resp.content
        """,
    )

    # ---------------------------
    # backend/app/services/chat_service.py
    # ---------------------------
    write_file(
        backend_app / "services" / "chat_service.py",
        """
        from backend.app.ai.llm_client import generate_reply


        def chat_reply(message: str) -> str:
            \"\"\"챗봇 비즈니스 로직 레이어.

            나중에 로그 저장, 사용량 카운트, 검열 로직 등을
            이 함수에 붙이면 된다.
            \"\"\"
            return generate_reply(message)
        """,
    )

    # ---------------------------
    # backend/app/api/routes.py
    # ---------------------------
    write_file(
        backend_app / "api" / "routes.py",
        """
        from fastapi import APIRouter
        from pydantic import BaseModel

        from backend.app.services.chat_service import chat_reply


        router = APIRouter()


        class ChatRequest(BaseModel):
            message: str


        class ChatResponse(BaseModel):
            reply: str


        @router.post("/chat", response_model=ChatResponse)
        async def chat_endpoint(payload: ChatRequest):
            \"\"\"AI와 대화하는 기본 챗 엔드포인트\"\"\"
            reply = chat_reply(payload.message)
            return ChatResponse(reply=reply)
        """,
    )

    # ---------------------------
    # backend/app/main.py
    # ---------------------------
    write_file(
        backend_app / "main.py",
        """
        from pathlib import Path

        from fastapi import FastAPI, Request
        from fastapi.staticfiles import StaticFiles
        from fastapi.templating import Jinja2Templates

        from backend.app.api.routes import router as api_router
        from backend.app.config.settings import settings


        BASE_DIR = Path(__file__).resolve().parent.parent.parent

        app = FastAPI(title=settings.PROJECT_NAME)

        # 템플릿 & 정적 파일 설정
        templates = Jinja2Templates(directory=str(BASE_DIR / "frontend" / "templates"))
        app.mount(
            "/static",
            StaticFiles(directory=str(BASE_DIR / "frontend" / "static")),
            name="static",
        )

        # API 라우터 등록
        app.include_router(api_router, prefix="/api")


        @app.get("/")
        async def index(request: Request):
            \"\"\"기본 HTML 페이지(챗봇 UI)\"\"\"
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                },
            )
        """,
    )

    # ---------------------------
    # frontend/templates/index.html
    # ---------------------------
    write_file(
        ROOT / "frontend" / "templates" / "index.html",
        """
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8" />
            <title>AI Chat Demo</title>
            <link rel="stylesheet" href="/static/style.css" />
        </head>
        <body>
            <div class="chat-container">
                <h1>AI 챗봇 데모</h1>
                <div id="chat-window">
                    <!-- 메시지들이 여기 쌓인다 -->
                </div>
                <form id="chat-form">
                    <input
                        type="text"
                        id="message-input"
                        placeholder="AI에게 말을 걸어보세요..."
                        autocomplete="off"
                        required
                    />
                    <button type="submit">전송</button>
                </form>
            </div>

            <script src="/static/app.js"></script>
        </body>
        </html>
        """,
    )

    # ---------------------------
    # frontend/static/style.css
    # ---------------------------
    write_file(
        ROOT / "frontend" / "static" / "style.css",
        """
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
                sans-serif;
            background: #f5f5f5;
            margin: 0;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }

        .chat-container {
            background: #ffffff;
            width: 400px;
            max-width: 90vw;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        h1 {
            margin: 0 0 8px 0;
            font-size: 20px;
            text-align: center;
        }

        #chat-window {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 8px;
            height: 300px;
            overflow-y: auto;
            background: #fafafa;
            font-size: 14px;
        }

        .message {
            margin: 4px 0;
            padding: 6px 10px;
            border-radius: 10px;
            max-width: 85%;
        }

        .message.user {
            background: #007bff;
            color: #fff;
            margin-left: auto;
        }

        .message.bot {
            background: #e9ecef;
            color: #111;
            margin-right: auto;
        }

        #chat-form {
            display: flex;
            gap: 8px;
        }

        #message-input {
            flex: 1;
            padding: 8px;
            border-radius: 8px;
            border: 1px solid #ccc;
            font-size: 14px;
        }

        button {
            padding: 0 14px;
            border: none;
            border-radius: 8px;
            background: #007bff;
            color: white;
            cursor: pointer;
            font-size: 14px;
        }

        button:disabled {
            opacity: 0.7;
            cursor: default;
        }
        """,
    )

    # ---------------------------
    # frontend/static/app.js
    # ---------------------------
    write_file(
        ROOT / "frontend" / "static" / "app.js",
        """
        const form = document.getElementById("chat-form");
        const input = document.getElementById("message-input");
        const chatWindow = document.getElementById("chat-window");

        function appendMessage(text, sender = "user") {
            const div = document.createElement("div");
            div.classList.add("message", sender);
            div.textContent = text;
            chatWindow.appendChild(div);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }

        async function sendMessage(message) {
            appendMessage(message, "user");

            try {
                const res = await fetch("/api/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ message }),
                });

                if (!res.ok) {
                    appendMessage("서버 오류가 발생했습니다.", "bot");
                    return;
                }

                const data = await res.json();
                appendMessage(data.reply, "bot");
            } catch (e) {
                appendMessage("네트워크 오류가 발생했습니다.", "bot");
            }
        }

        form.addEventListener("submit", (e) => {
            e.preventDefault();
            const message = input.value.trim();
            if (!message) return;
            input.value = "";
            sendMessage(message);
        });
        """,
    )

    # ---------------------------
    # requirements.txt
    # ---------------------------
    write_file(
        ROOT / "requirements.txt",
        """
        fastapi
        uvicorn
        jinja2
        langchain
        langchain-openai
        """,
    )

    print("\\n구성이 완료되었습니다.")
    print("서버 실행 예시:")
    print("  uvicorn backend.app.main:app --reload")
    print("OPENAI_API_KEY 없으면 데모 에코 응답으로 동작합니다.")


if __name__ == "__main__":
    main()
