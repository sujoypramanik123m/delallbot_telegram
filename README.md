# Telegram Delete All Messages Bot

A Telegram bot to delete messages and broadcast messages in groups, supergroups, or channels.

## Features

- */start*: Logs new users and sends a welcome message with inline buttons.
- */delall*: Deletes all messages in the current group/channel (admin only).
- */delfrom*: Reply to a message and use this command to delete that message and all subsequent messages (admin only).
- */broadcast*: Reply to a message to broadcast it to all groups/channels where the bot is an admin (owner only).

## Requirements

- *Telegram API credentials* (`API_ID`, `API_HASH`)
- *Bot token* with admin privileges in the target group/channel.
- *MongoDB* for storing chat information.

## Setup

1. *Configure Environment Variables*: Ensure the following environment variables are set:
   - `API_ID`
   - `API_HASH`
   - `BOT_TOKEN`
   - `DB_URL`
   - `DB_NAME`
   - `LOG_CHANNEL_ID`
   - `OWNER_ID`

2. *Build and Run the Docker Container*:
   
