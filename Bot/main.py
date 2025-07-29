import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from consumer import consume_kafka  # import our kafka logic

# Replace with your handlers
async def start(update, context):
    await update.message.reply_text("Welcome! You’ll receive alerts for your subscribed pairs.")

async def run_bot():
    from telegram.ext import ApplicationBuilder
    app = ApplicationBuilder().token("YOUR_TOKEN_HERE").build()

    app.add_handler(CommandHandler("start", start))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    print("🚀 Telegram Bot started")
    await app.updater.idle()

async def main():
    await asyncio.gather(
        run_bot(),
        consume_kafka()
    )

if __name__ == "__main__":
    asyncio.run(main())
