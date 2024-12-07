from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# Replace with your bot token and chat ID
BOT_TOKEN = '7991575231:AAHybU6exZCmRgHk-kKQt22QvveVad2POp8'
BOT_USERNAME: Final = "syren0914_bot"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Thanks for chatting with me! I am a crypto price alert bot")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Type something and i will reply")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command!")


# Handle responses
def handle_responses(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return 'Hey there'
    if 'how are you' in processed:
        return " I am good"
    return "I dont understand :)"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type:str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type}: '{text}'")

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_responses(new_text)
        else:
            return
    else:
        response:str = handle_responses(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print('Starting bot ....')
    app = Application.builder().token(BOT_TOKEN).build()
    #commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error 
    app.add_error_handler(error)
    print("Polling ...")
    app.run_polling(poll_interval=3)