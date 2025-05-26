# Telegram Delete All Messages Bot

A Telegram bot to delete messages and broadcast messages in groups, supergroups, or channels.

## Features

- `/delall` - Deletes all messages in the current group/channel.
- `/delfrom` - Reply to a message and use this command to delete that message and all subsequent messages.
- `/broadcast` - Reply to a message to broadcast it to all groups/channels where the bot is an admin.

## Requirements

- Telegram API credentials (`API_ID`, `API_HASH`)
- Bot token with admin privileges in the target group/channel.
- MongoDB for storing chat information.
- Bot must have "Delete Messages" and "Send Messages" permissions.

## Setup

1. Replace `YOUR_API_ID`, `YOUR_API_HASH`, and `YOUR_BOT_TOKEN` in `config.py`.

2. Configure MongoDB connection in `config.py`.

3. Build Docker image: docker build -t telegram-delete-all-bot .

4. Run Docker container: docker run -d --name deleteall .
