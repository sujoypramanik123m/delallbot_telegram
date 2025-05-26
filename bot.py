import asyncio
import logging
from telethon import TelegramClient, events, errors
from telethon.tl.types import PeerChannel, PeerChat
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL
from broadcast import broadcast_message
from database import add_chat, get_all_chats, add_user

# Limit concurrent deletes to avoid hitting rate limits
CONCURRENT_DELETES = 10

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create client and start bot
client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def delete_messages(chat, message_ids):
    sem = asyncio.Semaphore(CONCURRENT_DELETES)

    async def delete_single(msg_id):
        async with sem:
            try:
                await client.delete_messages(chat, msg_id)
            except errors.MessageDeleteForbiddenError:
                logger.warning(f'No permission to delete message {msg_id} in {chat}')
            except Exception as e:
                logger.error(f'Failed to delete message {msg_id}: {e}')

    await asyncio.gather(*(delete_single(msg_id) for msg_id in message_ids))

def is_group_or_channel(chat):
    return isinstance(chat, (PeerChannel, PeerChat))

@client.on(events.NewMessage(pattern='/delall'))
async def handler_delall(event):
    chat = await event.get_input_chat()
    sender = await event.get_sender()

    if not is_group_or_channel(chat):
        await event.reply("This command only works in groups, supergroups, or channels.")
        return

    perms = await client.get_permissions(chat, sender)
    if not perms.is_admin:
        await event.reply("You need to be admin to use this command.")
        return

    me = await client.get_me()
    bot_perms = await client.get_permissions(chat, me)
    if not bot_perms.delete_messages:
        await event.reply("I need 'Delete Messages' permission to delete messages.")
        return

    await event.respond("Starting to delete all messages...")

    message_ids = []
    async for msg in client.iter_messages(chat):
        message_ids.append(msg.id)

    await delete_messages(chat, message_ids)
    await event.respond(f"Deleted {len(message_ids)} messages in chat!")

@client.on(events.NewMessage(pattern='/delfrom'))
async def handler_delfrom(event):
    if not event.is_reply:
        await event.reply("Please reply to the message from which you want to start deleting.")
        return

    chat = await event.get_input_chat()
    sender = await event.get_sender()

    if not is_group_or_channel(chat):
        await event.reply("This command only works in groups, supergroups, or channels.")
        return

    perms = await client.get_permissions(chat, sender)
    if not perms.is_admin:
        await event.reply("You need to be admin to use this command.")
        return

    me = await client.get_me()
    bot_perms = await client.get_permissions(chat, me)
    if not bot_perms.delete_messages:
        await event.reply("I need 'Delete Messages' permission to delete messages.")
        return

    reply_msg = await event.get_reply_message()
    start_id = reply_msg.id

    await event.respond(f"Deleting from message ID {start_id} onwards...")

    message_ids = []
    async for msg in client.iter_messages(chat, offset_id=start_id - 1, reverse=True):
        if msg.id >= start_id:
            message_ids.append(msg.id)

    if not message_ids:
        await event.respond("No messages found to delete from that message onwards.")
        return

    await delete_messages(chat, message_ids)
    await event.respond(f"Deleted {len(message_ids)} messages starting from message ID {start_id}.")

@client.on(events.NewMessage(pattern='/broadcast'))
async def handler_broadcast(event):
    if not event.is_reply:
        await event.reply("Please reply to the message you want to broadcast.")
        return

    reply_msg = await event.get_reply_message()
    message_to_broadcast = reply_msg.text

    chats = get_all_chats()
    await broadcast_message(client, chats, message_to_broadcast)
    await event.reply("Broadcast completed!")

@client.on(events.NewMessage)
async def handler_new_user(event):
    user = await event.get_sender()
    add_user(user)
    # Send notification to log channel
    await client.send_message(LOG_CHANNEL, f"New user started the bot:\nID: {user.id}\nName: {user.first_name} {user.last_name or ''}\nUsername: @{user.username or 'N/A'}")

async def main():
    print("Bot is up and running...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
