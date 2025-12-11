from fastapi import FastAPI

from app.chat.adapter.inbound.api.router import router as chat_router

app = FastAPI(title="Sokdak AI API", version="0.1.0")


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(chat_router)
