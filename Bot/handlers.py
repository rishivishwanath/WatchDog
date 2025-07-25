from telegram import Update
from telegram.ext import ContextTypes
from db import subscribe_user

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Welcome to Arbitrage Bot!")

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if context.args:
        subscribe_user(chat_id, context.args)
        await update.message.reply_text(f"✅ Subscribed to: {', '.join(context.args)}")
    else:
        await update.message.reply_text("❌ Usage: /subscribe BTC ETH")
