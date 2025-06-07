#%%
import sys, os
# Add the location of the utils folder to the system path
utils_folder_path = os.path.join(os.path.dirname(__file__), "utils")
sys.path.append(utils_folder_path)

from openai import OpenAI 
from pydantic import BaseModel, ConfigDict
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta
from notion_client import Client as NotionClient

from config import *

#%%

# Initialize OpenAI and Notion clients using API keys from environment variables
open_ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
not_client = NotionClient(auth=os.getenv("NOTION_API_KEY"))

#%%
def get_day_of_week(date_str):
    """
    Returns the first three characters of the day of the week for a given date string.

    Args:
        date_str (str): Date string in the format 'YYYY-MM-DD'.

    Returns:
        str: First three characters of the day of the week (e.g., 'Mon', 'Tue').
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj.strftime("%a")

def get_financial_week_number(date_str):
    """
    Returns the financial week number for a given date string.
    Financial week starts from the first Monday of the year.

    Args:
        date_str (str): Date string in the format 'YYYY-MM-DD'.

    Returns:
        int: Financial week number.
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
    Returns today's date as a string in the format 'YYYY-MM-DD'.

    Returns:
        str: Today's date in 'YYYY-MM-DD' format.
    """
    return datetime.now().strftime("%Y-%m-%d")

def write_row(client, database_id, data):
    """
    Writes a row to the Notion database with the provided data.

    Args:
        client (NotionClient): Notion client instance.
        database_id (str): ID of the Notion database.
        data (list): List of dictionaries containing row data to be added.

    Returns:
        None
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

# Create the Pydantic class for workout data validation
class WorkoutData(BaseModel):
    """
    Pydantic model for validating workout data.
    """
    model_config = ConfigDict(extra='forbid')  # Forbid extra fields not defined in the schema

    setnum: int
    exercise: str
    muscle_group: str
    weight: int
    reps: int 

# Generate JSON schema for the workout data model
schema = WorkoutData.model_json_schema()

#%%
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle incoming messages from the Telegram bot.

    Args:
        update (Update): Telegram update object containing the message.
        context (ContextTypes.DEFAULT_TYPE): Context object for the bot.

    Returns:
        None
    """
    user_message = update.message.text
    response = ""

    # Generate a response using OpenAI's API
    response = open_ai_client.responses.create(
        model="gpt-4o-mini",
        instructions="Extract the workout data from the user message and clean the exercise name",
        input=user_message,
        text={
            "format": {
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
            }
        ]
        write_row(not_client, DATABASE_ID, data)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Successfully added row: {response.output_text}")

    return 

def main():
    # Build the Telegram bot application
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
