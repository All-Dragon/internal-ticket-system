import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.api.routers import ticket_router, authorization_router
from app.core.logging_config import setup_logging

setup_logging()

APP_VERSION = "0.1.0"
SERVICE_NAME = "Internal Ticket System API"

app = FastAPI(
    title=SERVICE_NAME,
    version=APP_VERSION,
    description="API for internal ticket management.",
)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", include_in_schema=False)
async def health():
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "version": APP_VERSION,
    }

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def main_menu():
    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{SERVICE_NAME}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #f5f7fa;
                    padding: 40px;
                }}
                .card {{
                    max-width: 600px;
                    margin: auto;
                    background: white;
                    padding: 30px;
                    border-radius: 12px;
                    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
                }}
                .meta {{
                    color: #6b7280;
                    font-size: 14px;
                    margin-bottom: 20px;
                }}
                a {{
                    display: block;
                    margin: 10px 0;
                    text-decoration: none;
                    color: #2563eb;
                    font-weight: 500;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>{SERVICE_NAME}</h1>
                <div class="meta">
                    Version: <strong>{APP_VERSION}</strong><br>
                    Status: <span style="color: green;">online</span>
                </div>
                <p>Internal ticket management API.</p>
                <h3>Navigation</h3>
                <a href="/docs">Swagger UI</a>
                <a href="/redoc">ReDoc</a>
                <a href="/health">Health check</a>
            </div>
        </body>
        </html>
        """

app.include_router(router=ticket_router)
app.include_router(router=authorization_router)