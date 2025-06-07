#%%
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from notion_client import Client as NotionClient

# from langchain.chat_models import ChatOpenAI
# from langchain.schemas import HumanMessage, AIMessage, SystemMessage 

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime
#%%

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
not_client = NotionClient(auth=os.getenv("NOTION_API_KEY"))
#%%
def get_notion_database(database_id: str):
    try:
        db = not_client.databases.retrieve(database_id = DATABASE_ID)
        pages = not_client.databases.query(database_id=DATABASE_ID)["results"]
        props = not_client.databases.retrieve(database_id=DATABASE_ID)["properties"]
        # print (f"DB: {db}")
        # print (f"Pages: {pages}")
        print (f"Properties: {props}")
        return props
    except Exception as e:
        print(f"Error retrieving Notion database: {e}")
        
#%%
props = get_notion_database(DATABASE_ID)

# %%

    

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



data = [
    {
        "date": get_todays_date(),
        "dayofweek": get_day_of_week(get_todays_date()),
        "weeknum": get_financial_week_number(get_todays_date()),
        "setnum": 1,
        "exercise": "Bench Press",
        "group": "Chest",
        "weight": 100,
        "reps": 10,
        "one_rm": 120,
        "notes": "Felt strong today",
    },
    {
        "date": get_todays_date(),
        "dayofweek": get_day_of_week(get_todays_date()),
        "weeknum": get_financial_week_number(get_todays_date()),
        "setnum": 2,
        "exercise": "Squat",
        "group": 'Legs',
        "weight": 150,
        "reps": 8,
        "one_rm": 180,
        "notes": "Challenging but good form",
    },
]
#%%
write_row(not_client, DATABASE_ID, data)
#%%
if __name__ == '__main__':
    main()

# %%
