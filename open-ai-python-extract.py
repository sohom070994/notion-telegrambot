#%%
import os
from dotenv import load_dotenv
from openai import OpenAI
# from langchain.chat_models import ChatOpenAI
# from langchain.schemas import HumanMessage, AIMessage, SystemMessage 
from pydantic import BaseModel, ConfigDict
from typing import List 
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta

from notion_client import Client as NotionClient

load_dotenv()
# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NOTION_ENDPOINT = os.getenv("NOTION_ENDPOINT")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")
DATABASE_ID = os.getenv("DATABASE_ID")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
not_client = NotionClient(auth=os.getenv("NOTION_API_KEY"))
#%%
def get_day_of_week(date_str):
    """
    Returns the first three characters of the day of the week for a given date string.
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%a")

def get_financial_week_number(date_str):
    """
    Returns the financial week number for a given date string.
    Financial week starts from the first Monday of the year.
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    year_start = datetime(date_obj.year, 1, 1)
    # Find the first Monday of the year
    first_monday = year_start + timedelta(days=(7 - year_start.weekday()) % 7)
    if date_obj < first_monday:
        return 52  # Consider dates before the first Monday as part of the last year's week 52
    return ((date_obj - first_monday).days // 7) + 1



def get_todays_date():
    """
    Returns today's date as a string in the format YYYY-MM-DD.
    """
    return datetime.now().strftime("%Y-%m-%d")

def write_row(client, database_id, data):
    """
    Writes a row to the Notion database with the provided data.
    """
    for entry in data:
        try:
            client.pages.create(
                **{
                    "parent": {"database_id": database_id},
                    "properties": {
                        "Date": {"title": [{"text": {"content": entry["date"]}}]},
                        "DayOfWeek": {"rich_text": [{"text": {"content": entry["dayofweek"]}}]},
                        "Week": {"number": entry["weeknum"]},
                        "Set": {"number": entry["setnum"]},
                        "Exercise": {"rich_text": [{"text": {"content": entry["exercise"]}}]},
                        "Group": {"rich_text": [{"text": {"content": entry["group"]}}]},
                        "Weight": {"number": entry["weight"]},
                        "Reps": {"number": entry["reps"]},
                        "1RM": {"number": entry["one_rm"]},
                        "Notes": {"rich_text": [{"text": {"content": entry["notes"]}}]},
                    },
                }
            )
            print(f"Row added successfully: {entry}")
        except Exception as e:
            print(f"Error adding row: {e}")


# create the Pydantic class
class WorkoutData(BaseModel):
    model_config = ConfigDict(extra ='forbid')  # Forbid extra fields not defined in the schema

    setnum: int
    exercise: str
    muscle_group: str
    weight: int
    reps: int 

schema = WorkoutData.model_json_schema()    

# print("Schema for workout data:")
# print(schema)

#%%
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages."""
    user_message = update.message.text
    response = ""

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": user_message},
        ],
    )
    # response = completion.choices[0].message.content

    response = client.responses.create(
        model="gpt-4o-mini",
        instructions= "Extract the workout data from the user message and clean the exercise name",
        input=user_message,
        text = {
            "format" : {
                "type": "json_schema",
                "name": "workout_data",
                "schema": schema,
                "strict": True
            }
        }
    )

    if response:    
        response_data = json.loads(response.output_text)
        data = [
            {
            "date": get_todays_date(),
            "dayofweek": get_day_of_week(get_todays_date()),
            "weeknum": get_financial_week_number(get_todays_date()),
            "setnum": response_data['setnum'],
            "exercise": response_data['exercise'],
            "group": response_data['muscle_group'],
            "weight": response_data['weight'],
            "reps": response_data['reps'],
            "one_rm": response_data['weight'] * (1 + response_data['reps'] / 30),  # Epley formula for 1RM
            "notes": "Felt strong today",
            }]
        write_row(not_client, DATABASE_ID, data)
        await context.bot.send_message(chat_id=update.effective_chat.id, text= f"Succesfully added row: {response.output_text}")

    return 

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", handle_message))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
#%%

# Structured Output mode
input_messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": "exercise is db bench press, weight is 45, reps is 5"
            },
        ]
    }
]
# %%
response = client.responses.create(
    model="gpt-4o-mini",
    instructions= "Extract the workout data from the user message and clean the exercise name",
    input = input_messages,
    text = {
        "format" : {
            "type": "json_schema",
            "name": "workout_data",
            "schema": schema,
            "strict": True
        }
    }
)
 #%%
print("Response from OpenAI:")
print(response.output_text)
# # %%

# %%
