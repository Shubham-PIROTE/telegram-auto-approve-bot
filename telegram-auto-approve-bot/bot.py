import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ContextTypes
)

# 🔐 BOT TOKEN (from environment variable)
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")

# 🚀 AUTO APPROVE JOIN REQUESTS
async def auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    join_request = update.chat_join_request

    await join_request.approve()

    # Optional welcome message
    try:
        await context.bot.send_message(
            chat_id=join_request.user_chat_id,
            text="✅ Your request to join the channel has been approved!"
        )
    except:
        pass

    print(
        f"Approved user {join_request.from_user.id} "
        f"in chat {join_request.chat.id}"
    )

# 🤖 BOT SETUP
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(ChatJoinRequestHandler(auto_approve))

print("🤖 Auto-approve channel bot is running...")
app.run_polling()
