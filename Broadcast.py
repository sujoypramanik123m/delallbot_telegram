async def broadcast_message(client, chats, message):
    for chat_id in chats:
        try:
            await client.send_message(chat_id, message)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")
