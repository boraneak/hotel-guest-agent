import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes,
)
from agent.rag import build_qa_chain
from agent.router import route_property
from agent.memory import get_memory

load_dotenv()

# Cache QA chains per property
_chains: dict = {}


def get_chain(property_key: str):
    if property_key not in _chains:
        _chains[property_key] = build_qa_chain(property_key)
    return _chains[property_key]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Hotel Guest Agent!\n\n"
        "I can answer questions about:\n"
        "🏨 *Grandview Hotel & Resort*\n"
        "🍜 *Golden Spoon Restaurant*\n"
        "🏖️ *Azure Beach Resort*\n\n"
        "Just ask me anything! For example:\n"
        "• What time does Golden Spoon close?\n"
        "• Does Azure Beach have a pool?\n"
        "• What are the room prices at Grandview Hotel?",
        parse_mode="Markdown",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    message = update.message.text

    try:
        # 1. Route
        property_key = route_property(message)

        # 2. Get memory
        memory = get_memory(user_id)
        history = memory.load_memory_variables({}).get("chat_history", [])

        # 3. Build context from history
        history_text = ""
        for msg in history:
            role = "Guest" if msg.type == "human" else "Assistant"
            history_text += f"{role}: {msg.content}\n"

        # 4. Answer
        chain = get_chain(property_key)
        full_question = f"{history_text}Guest: {message}" if history_text else message
        answer = chain(full_question)

        # 5. Save to memory
        memory.save_context({"input": message}, {"output": answer})

        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(
            "Sorry, I'm having trouble processing your request right now. "
            "Please try again in a moment."
        )
