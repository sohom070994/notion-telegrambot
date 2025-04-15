#%%
import os
from dotenv import load_dotenv
from openai import OpenAI
# from langchain.chat_models import ChatOpenAI
# from langchain.schemas import HumanMessage, AIMessage, SystemMessage 

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#%%



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages."""
    user_message = update.message.text
    response = ""

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_message},
        ],
    )
    response = completion.choices[0].message.content

    if response:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    return 

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", handle_message))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()