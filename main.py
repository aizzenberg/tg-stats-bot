import asyncio
import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from telegram import Update

from services.bot_service import BotService
from services.env_service import get_env_var

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

bot_app = BotService.run_telegram_bot()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Set the webhook when the app starts"""
    WEBHOOK_URL = get_env_var("WEBHOOK_URL")
    logger.info(f"Setting webhook to {WEBHOOK_URL}")

    await bot_app.bot.set_webhook(WEBHOOK_URL)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def webhook(request: Request):
    """Handle incoming Telegram updates"""
    data = await request.json()
    update = Update.de_json(data, bot_app.bot)
    await bot_app.process_update(update)
    return {"status": "ok"}


@app.get("/")
def root():
    """Root endpoint for testing"""
    return {"message": "Bot is running!"}


def main():
    """Start the webhook server"""
    PORT = int(get_env_var("PORT", 8080))

    logger.info(f"Starting bot on port {PORT}...")

    uvicorn.run(app, host='0.0.0.0', port=PORT)


if __name__ == '__main__':
    main()
