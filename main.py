import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from telegram.request import HTTPXRequest
from bot.telegram_bot import start, handle_message
import uvicorn

load_dotenv(override=False)

# FastAPI app
app = FastAPI(title="Hotel Guest Agent")


@app.get("/")
async def root():
    return {"status": "ok", "message": "Hotel Guest Agent is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


def build_bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
    )
    application = ApplicationBuilder().token(token).request(request).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    return application


async def run():
    bot = build_bot()

    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)

    async with bot:
        await bot.start()
        await bot.updater.start_polling()
        await server.serve()
        await bot.updater.stop()
        await bot.stop()


if __name__ == "__main__":
    asyncio.run(run())
