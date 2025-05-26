# bot.py

import asyncio
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
from config import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL_ID, OWNER_ID
from database import add_user, get_all_chats, add_chat
from broadcast import broadcast_message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def is_admin(chat_id, user_id):
    try:
        participant = await client(GetParticipantRequest(chat_id, user_id))
        return isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator))
    except:
        return False

@client.on(events.NewMessage(pattern='/start'))
async def handler_start(event):
    user = await event.get_sender()
    add_user(user)
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton('✚ Add Me In Your Group ✚', url='https://t.me/DelAll_ProBot?startgroup=true')],
        [InlineKeyboardButton('❣️ Developer ❣️', url='https://t.me/UncleChipssBot')],
        [InlineKeyboardButton('🔍 Support Group', url='https://t.me/SuperToppers0'),
         InlineKeyboardButton('🤖 Update Group', url='https://t.me/SuperToppers')],
        [InlineKeyboardButton('💝 Subscribe My YouTube Channel', url='https://youtube.com/@SuperToppers')]
    ])
    await client.send_message(
        event.chat_id,
        f"Hi {user.first_name}✨, I am Delall bot, I'm a bot that can delete all your channel or supergroup messages.\n"
        "To use me:\n"
        "- add me to the channel/supergroup as admin (with at least delete messages, invite users and add admins permissions)\n"
        "- send /delall if you want all the messages to be deleted\n"
        "- send /delfrom in reply to a message if you want to delete that and all subsequent messages\n\n"
        "In case of issues, contact @UncleChipssBot",
        buttons=buttons
    )
    await client.send_message(
        LOG_CHANNEL_ID,
        f"𝖭𝖾𝗐 𝖴𝗌𝖾𝗋 𝖲𝗍𝖺𝗋𝗍𝖾𝖽 𝖳𝗁𝖾 𝖡𝗈𝗍\n\n"
        f"𝖴𝗌𝖾𝗋 𝖬𝖾𝗇𝗍𝗂𝗈𝗇: {user.first_name} {user.last_name or ''}\n"
        f"𝖴𝗌𝖾𝗋 𝖨𝖣: {user.id}\n"
        f"𝖥𝗂𝗋𝗌𝗍 𝖭𝖺𝗆𝖾: {user.first_name}\n"
        f"𝖫𝖺𝗌𝗍 𝖭𝖺𝗆𝖾: {user.last_name or 'None'}\n"
        f"𝖴𝗌𝖾𝗋 𝖭𝖺𝗆𝖾: @{user.username or 'None'}\n"
        f"𝖴𝗌𝖾𝗋 𝖫𝗂𝗇𝗄: [Click Here](tg://user?id={user.id})\n\n"
        f"𝖣𝖺𝗍𝖾: {datetime.now().strftime('%d %B, %Y')}\n"
        f"𝖳𝗂𝗆𝖾: {datetime.now().strftime('%I:%M:%S %p')}"
    )

@client.on(events.NewMessage(pattern='/delall'))
async def handler_delall(event):
    if not await is_admin(event.chat_id, event.sender_id):
        await event.reply("You must be an admin to use this command.")
        return

    chat = await event.get_chat()
    add_chat(chat.id)
    async for message in client.iter_messages(chat):
        await message.delete()
    await event.reply("All messages deleted.")

@client.on(events.NewMessage(pattern='/delfrom'))
async def handler_delfrom(event):
    if not await is_admin(event.chat_id, event.sender_id):
        await event.reply("You must be an admin to use this command.")
        return

    if not event.is_reply:
        await event.reply("Please reply to the message you want to delete from.")
        return

    chat = await event.get_chat()
    add_chat(chat.id)
    reply_msg = await event.get_reply_message()
    async for message in client.iter_messages(chat, min_id=reply_msg.id):
        await message.delete()
    await event.reply("Messages deleted from the specified point.")

@client.on(events.NewMessage(pattern='/broadcast'))
async def handler_broadcast(event):
    if event.sender_id != OWNER_ID:
        await event.reply("You are not authorized to use this command.")
        return

    if not event.is_reply:
        await event.reply("Please reply to the message you want to broadcast.")
        return

    reply_msg = await event.get_reply_message()
    message_to_broadcast = reply_msg.text
    chats = get_all_chats()
    await broadcast_message(client, chats, message_to_broadcast)
    await event.reply("Broadcast completed!")

async def main():
    print("Bot is up and running...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
