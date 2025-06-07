# Notion Telegram Bot

This project integrates Notion, OpenAI, and Telegram to create a bot that interacts with users and performs various tasks using these services.

## Project Structure

- `basic-telegrambot.py`: Contains the basic implementation of the Telegram bot.
- `notion-app.py`: Handles interactions with the Notion API.
- `open-ai.py`: Manages communication with the OpenAI API.
- `tools.py`: Contains utility functions used across the project.
- `requirements.txt`: Lists the dependencies required for the project.
- `.env`: Stores sensitive configuration details.

## Setting Up the .env File

The `.env` file should contain the following keys:

```
TELEGRAM_TOKEN=<Your Telegram Bot Token>
OPENAI_API_KEY=<Your OpenAI API Key>
NOTION_API_KEY=<Your Notion API Key>
NOTION_ENDPOINT=https://api.notion.com/v1
NOTION_PAGE_ID=<Your Notion Page ID>
DATABASE_ID=<Your Notion Database ID>
```

### How to Obtain the Keys

1. **Telegram Token**:

   - Create a bot using the [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
   - Follow the instructions to get your bot token.
2. **OpenAI API Key**:

   - Sign up or log in to [OpenAI](https://platform.openai.com/).
   - Navigate to the API section to generate your API key.
3. **Notion API Key and IDs**:

   - Log in to [Notion](https://www.notion.so/).
   - Go to [Notion Developers](https://www.notion.so/my-integrations) and create an integration to get your API key.
   - Share your Notion page or database with the integration to get the `NOTION_PAGE_ID` and `DATABASE_ID`.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:

   ```bash
   cd notion_telegrambot
   ```
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add the required keys as described above.

## Running the Bot

Run the main script to start the bot:

```bash
python open-ai.py
```

## Updating the Notion Database

The `query_notion.py` script includes functionality to update a Notion database. It provides the following features:

1. **Retrieve Database Properties**:

   - The `get_notion_database` function retrieves the properties of a specified Notion database.
2. **Write Rows to the Database**:

   - The `write_row` function allows you to add rows to the Notion database with structured data. Each row includes details such as date, day of the week, exercise, weight, and notes.

### Example Usage

To update the Notion database, ensure the `.env` file is correctly configured with the `DATABASE_ID` and other required keys. Then, run the script to add data entries to the database.

## License

This project is licensed under the MIT License.
