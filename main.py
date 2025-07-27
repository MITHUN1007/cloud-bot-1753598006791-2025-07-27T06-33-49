from telethon import TelegramClient, events
import os
from groq import Groq

# Your API ID, hash, and bot token from Telegram
API_ID = int(os.environ.get("TELEGRAM_API_ID"))
API_HASH = os.environ.get("TELEGRAM_API_HASH")
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
groq_client = Groq(api_key=GROQ_API_KEY)

@client.on(events.NewMessage)
async def echo(event):
    try:
        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": event.message.message}],
            max_tokens=1024,
        )
        await event.reply(response.choices[0].message.content)
    except Exception as e:
        await event.reply(f"Error processing message: {str(e)}")

if __name__ == '__main__':
    print("Bot started. Stop with Ctrl+C")
    client.run_until_disconnected()