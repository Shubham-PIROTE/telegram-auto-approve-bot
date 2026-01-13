import os
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")

async def auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jr = update.chat_join_request
    try:
        await jr.approve()
        print(f"Approved user {jr.from_user.id}")
    except BadRequest:
        pass

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(ChatJoinRequestHandler(auto_approve))

print("Bot running...")
app.run_polling()
