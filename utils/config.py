from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NOTION_ENDPOINT = os.getenv("NOTION_ENDPOINT")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")
DATABASE_ID = os.getenv("DATABASE_ID")