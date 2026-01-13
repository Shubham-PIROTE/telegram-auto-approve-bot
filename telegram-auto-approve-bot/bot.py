import os
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    ContextTypes
)

# Read token from environment
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")

async def auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jr = update.chat_join_request

    try:
        await jr.approve()
        print(f"✅ Approved user {jr.from_user.id} in chat {jr.chat.id}")

        try:
            await context.bot.send_message(
                chat_id=jr.user_chat_id,
                text="✅ Your request to join the channel has been approved!"
            )
        except:
            pass

    except BadRequest as e:
        if "USER_ALREADY_PARTICIPANT" in str(e).upper():
            pass
        else:
            print("⚠️ Error:", e)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(ChatJoinRequestHandler(auto_approve))

print("🤖 Auto-approve channel bot is running...")
app.run_polling()
