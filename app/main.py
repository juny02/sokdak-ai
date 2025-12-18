from fastapi import FastAPI

from app.character.adapter.inbound.api.error_handlers import character_error_handlers
from app.character.adapter.inbound.api.router import router as character_router
from app.chat.adapter.inbound.api.error_handlers import chat_error_handlers
from app.chat.adapter.inbound.api.router import router as chat_router

app = FastAPI(title="Sokdak AI API", version="0.1.0")

for exc, handler in {
    **chat_error_handlers,
    **character_error_handlers,
}.items():
    app.add_exception_handler(exc, handler)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(chat_router)
app.include_router(character_router)
