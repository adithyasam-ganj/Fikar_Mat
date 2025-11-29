# Fikar_Mat_MumbaiHacks
A private, friendly companion on Telegram that coaching institutes can partner with  to take care of the mental health of their students.


# Recent model

- *Telegram_bot_agent_sys* is the latest file with the agent system framework developed.

- *Hing-Roberta* is the model training notebook


# Running the Files

- Bot Link: https://t.me/Arpan1stBot
- The bot is running. You can simply start with a *Hello* or anything to start the conversation

- You can use *Telegram_bot_agent_sys.ipynb* to create your own agentic system after creating a Telegram bot.
- *Telegram_bot_agent_sys.ipynb* needs the *db_models.py* file as it has the database models and the *institute_dashboard.py* file, which contains the streamlit dashboard. For running the Streamlit dashboard just use *streamlit run institute_dashboard.py*.

# Telegram Bot Setup (BotFather & API Key)

This guide explains how to create a Telegram bot using **BotFather** and get its **API token** (bot API key).

---

# Creating a Bot

- A Telegram account
- Telegram app installed (mobile or desktop)

---

## 1. Find BotFather

1. Open Telegram.
2. In the search bar, type `BotFather`.
3. Select the verified account named **“BotFather”** with a blue check mark.

---

## 2. Start a Chat With BotFather

1. Open the BotFather chat.
2. Click **Start** (or type `/start`).

---

## 3. Create a New Bot

1. In the BotFather chat, type:
   ```text
   /newbot

If the username is available, BotFather will create the bot and send a message with:

Example link to your bot (e.g. https://t.me/MyCoolBot)

Your bot token (API key), e.g.: 1234567890:AAH-ExampleTokenTextHere
