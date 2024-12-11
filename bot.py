import requests
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from decimal import Decimal
import os 
from dotenv import load_dotenv
load_dotenv()
# Set up your bot token
bot_token = os.getenv('BOT_TOKEN')
chat_id = os.getenv('CHANNEL_ID')  # Use your chat ID here

# Function to fetch the current price of any cryptocurrency
def get_crypto_price(coin_name: str):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={coin_name}&vs_currencies=usd'
    response = requests.get(url)
    data = response.json()
    # Check if the coin is valid
    if coin_name in data:
        return data[coin_name]['usd']
    else:
        return None

# Function to handle the /price command to get the price of a specific cryptocurrency
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        coin_name = context.args[0].lower()  # Get the coin name from the user's input
        price = get_crypto_price(coin_name)
        if price:
            await update.message.reply_text(f"The current price of {coin_name} is: ${price}")
        else:
            await update.message.reply_text(f"Sorry, I couldn't find the price for {coin_name}. Please check the coin name.")
    else:
        await update.message.reply_text("Please provide the name of the cryptocurrency. Example: /price bitcoin")

# Function to track the price change of a specific cryptocurrency
async def track_price_change(coin_name: str, percentage_change: Decimal):
    previous_price = get_crypto_price(coin_name)
    if previous_price is None:
        print("Coin not found.")
        return

    while True:
        await asyncio.sleep(60)  # Check the price every 60 seconds

        current_price = get_crypto_price(coin_name)
        if current_price is None:
            print("Coin not found.")
            continue

        price_change = (Decimal(current_price) - Decimal(previous_price)) / Decimal(previous_price) * 100

        if abs(price_change) >= percentage_change:
            # Send a notification to the user if the price changes by the specified percentage
            notification_message = f"The price of {coin_name} has changed by {price_change:.2f}%.\nCurrent price: ${current_price}"
            await send_notification(notification_message)
            previous_price = current_price  # Update the previous price

# Function to send a notification to the user
async def send_notification(message: str):
    # Use your chat ID to send the notification to yourself
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(f"Notification sent: {message}")
    else:
        print("Failed to send notification")

# Function to handle /status command to check if the bot is running
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("The bot is running smoothly!")

# Start tracking the price of a specific coin (for example, Bitcoin)
async def main():
    # Define which coin you want to track and the price change percentage
    coin_to_track = 'bitcoin'  # Change this to any coin you want to track
    price_change_percentage = Decimal('5')  # Set the percentage change threshold

    # Start tracking price changes in the background
    asyncio.create_task(track_price_change(coin_to_track, price_change_percentage))

    # Create an Application object with your bot token
    application = Application.builder().token(bot_token).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("price", price))  # /price will show the current price of a coin
    application.add_handler(CommandHandler("status", status))  # /status will show if the bot is running

    # Start the bot
    await application.run_polling()

# Use the already running event loop
if __name__ == '__main__':
    application = Application.builder().token(bot_token).build()
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("status", status))

    # Start polling for messages from Telegram without calling asyncio.run() or creating a new loop
    application.run_polling()
