from telegram.ext import ApplicationBuilder, CommandHandler
import logging
from config import TOKEN
from db import add_subscriber, remove_subscriber
import asyncio
import signal
import sys

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = TOKEN

async def start(update, context):
    await update.message.reply_text("👋 Welcome! Use /subscribe <pair> <min_lot> <min_percentage> to get alerts.\nExample:\n/subscribe BTC/USDT 0.001 2.5")

async def test_notify(update, context):
    await update.message.reply_text("✅ Test message from bot!")

async def subscribe(update, context):
    chat_id = update.effective_chat.id
    args = context.args

    if len(args) != 3:
        await update.effective_message.reply_text("⚠️ Usage: /subscribe <pair> <min_lot> <min_percentage>")
        return

    pair_name = args[0]
    try:
        min_lot = float(args[1])
        min_percentage = float(args[2])
    except ValueError:
        await update.effective_message.reply_text("⚠️ Please provide valid numbers for min_lot and min_percentage.")
        return

    add_subscriber(chat_id, pair_name, min_lot, min_percentage)
    await update.effective_message.reply_text(
        f"✅ Subscribed to {pair_name} with min_lot={min_lot}, min_percentage={min_percentage}%."
    )

async def unsubscribe(update, context):
    chat_id = update.effective_chat.id
    args = context.args

    if not args:
        # Remove all subscriptions for the user
        remove_subscriber(chat_id)
        await update.message.reply_text("🛑 You have been unsubscribed from all pairs.")
    else:
        pair_name = args[0]
        remove_subscriber(chat_id, pair_name)
        await update.message.reply_text(f"🛑 You have been unsubscribed from {pair_name}.")


def main():
    print("✅ Bot is starting...")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test_notify))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))

    print("🚀 Bot is now running! Press Ctrl+C to stop.")
    
    # Use run_polling without asyncio.run()
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped!")
    except Exception as e:
        print(f"❌ Error: {e}")