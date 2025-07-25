from telegram import Update
from telegram.ext import ContextTypes
from db import subscribe_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Welcome to Arbitrage Bot! Send Messages as /subscribe and pair1_pair2")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if context.args:
        pairs = [pair.lower() for pair in context.args]  # normalize to lowercase
        subscribe_user(chat_id, pairs)
        await update.message.reply_text(f"✅ Subscribed to: {', '.join(pairs)}")
    else:
        await update.message.reply_text("❌ Usage: /subscribe BTC ETH")

