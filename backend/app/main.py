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
    """기본 HTML 페이지(챗봇 UI)"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )
