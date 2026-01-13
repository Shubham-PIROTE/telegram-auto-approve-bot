import os
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ContextTypes
)

# ================== BOT TOKEN ==================
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")

# ================== AUTO APPROVE JOIN REQUEST ==================
async def auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    join_request = update.chat_join_request

    try:
        # Approve the join request
        await join_request.approve()
        print(f"✅ Approved user {join_request.from_user.id} in chat {join_request.chat.id}")

        # Optional welcome message (may fail due to privacy settings)
        try:
            await context.bot.send_message(
                chat_id=join_request.user_chat_id,
                text="✅ Your request to join the channel has been approved!"
            )
        except:
            pass

    except BadRequest as e:
        # SILENT HANDLING: user already joined
        if "USER_ALREADY_PARTICIPANT" in str(e).upper():
            pass
        else:
            print("⚠️ Unexpected error:", e)

# ================== BOT SETUP ==================
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(ChatJoinRequestHandler(auto_approve))

print("🤖 Auto-approve channel bot is running...")
app.run_polling()
