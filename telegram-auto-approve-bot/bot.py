import os
from telegram import Update
from telegram.error import BadRequest, Forbidden
from telegram.ext import (
    ApplicationBuilder,
    ChatJoinRequestHandler,
    CommandHandler,
    ContextTypes,
)

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable not set")


# /start command (what bot can do)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "𝐖𝐡𝐚𝐭 𝐜𝐚𝐧 𝐭𝐡𝐢𝐬 𝐛𝐨𝐭 𝐝𝐨?\n\n"
        "No waiting. No manual approvals.\n\n"
        "I handle all your join requests automatically the moment they arrive.\n\n"
        "Add me as admin — and let automation do the heavy lifting.\n\n"
        "👉 Send /knowmore to know more"
    )
    await update.message.reply_text(text)


# /knowmore command (your example message)
async def knowmore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Hello 🤗\n\n"
        "Welcome buddy — you’re in the right place 👍🏻\n\n"
        "This smart little bot automatically approves all pending join requests for your Telegram channels, instantly and effortlessly.\n\n"
        "Add it as an admin, and let automation handle the rest."
    )
    await update.message.reply_text(text)


# Auto approve join requests + DM approved message
async def auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jr = update.chat_join_request
    user = jr.from_user

    try:
        # Approve join request
        await jr.approve()
        print(f"✅ Approved user {user.id} ({user.full_name})")

        approved_msg = (
            f"Hello {user.first_name} 👋\n\n"
            f"✅ Your request to join our channel has been approved.\n\n"
            f"📌 Send /start to know more\n"
            f"✨ Or send /knowmore"
        )

        # DM user (works only if user has started the bot at least once)
        try:
            await context.bot.send_message(chat_id=user.id, text=approved_msg)
        except Forbidden:
            print("⚠️ Can't DM user (user blocked bot or never started bot).")
        except Exception as e:
            print("⚠️ DM error:", e)

    except BadRequest as e:
        if "USER_ALREADY_PARTICIPANT" in str(e).upper():
            pass
        else:
            print("⚠️ Approve error:", e)


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("knowmore", knowmore))

    # Join request handler
    app.add_handler(ChatJoinRequestHandler(auto_approve))

    print("🤖 Auto-approve bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
