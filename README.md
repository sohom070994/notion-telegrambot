# Notion Telegram Bot

This project integrates Notion, OpenAI, and Telegram to create a bot that interacts with users and updates a Notion database with workout data extracted from user messages.

## Project Structure

- `telegram_to_notion_openai.py`: The main script that implements the Telegram bot, integrates with OpenAI for data extraction, and updates the Notion database.
- Other `.py` files: These are test files used for various purposes during development.

## Setting Up the .env File

The `.env` file should contain the following keys:

```
TELEGRAM_TOKEN=<Your Telegram Bot Token>
OPENAI_API_KEY=<Your OpenAI API Key>
NOTION_API_KEY=<Your Notion API Key>
DATABASE_ID=<Your Notion Database ID>
```

### How to Obtain the Keys

1. **Telegram Token**:

   - Create a bot using the [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
   - Follow the instructions to get your bot token.
2. **OpenAI API Key**:

   - Sign up or log in to [OpenAI](https://platform.openai.com/).
   - Navigate to the API section to generate your API key.
3. **Notion API Key and Database ID**:

   - Log in to [Notion](https://www.notion.so/).
   - Go to [Notion Developers](https://www.notion.so/my-integrations) and create an integration to get your API key.
   - Share your Notion database with the integration to get the `DATABASE_ID`.

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
python telegram_to_notion_openai.py
```

## Features

1. **Telegram Bot**:

   - Listens to user messages and extracts workout data.
2. **OpenAI Integration**:

   - Uses OpenAI's API to process user messages and extract structured workout data.
3. **Notion Database Update**:

   - Updates a Notion database with the extracted workout data, including fields like date, day of the week, exercise, weight, and reps.

## License

This project is licensed under the MIT License.
