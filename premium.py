import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import InviteToChannelRequest, EditBannedRequest
from telethon.tl.types import ChatBannedRights
from datetime import datetime, timedelta

# Bot API credentials
API_ID = '23086727'       # Replace with your Telegram API ID
API_HASH = '1d8775e7509f0cfc666934cf9e94220c'   # Replace with your Telegram API Hash
BOT_TOKEN = '7861659107:AAFqH8BH49VzKNzaI_74hwtQOm425j9onds'  # Replace with your bot token

# Channel and user configuration
CHANNEL_ID = '-1002499067718'  # Replace with your channel ID or username
premium_users = {}  # Dictionary to hold premium users with their removal task

# Initialize the Telegram client with Telethon
client = TelegramClient('session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

async def add_and_schedule_removal(user_id):
    """Add user to channel and schedule removal after 1 hour."""
    try:
        # Invite user to channel
        await client(InviteToChannelRequest(CHANNEL_ID, [user_id]))
        print(f"User {user_id} added to channel.")
        
        # Schedule removal after 1 hour
        removal_task = asyncio.create_task(remove_user_after_delay(user_id, 3600))
        premium_users[user_id] = removal_task  # Store task in case you need to cancel it
        print(f"Scheduled removal for {user_id} in 1 hour.")
    except Exception as e:
        print(f"Error adding user {user_id}: {e}")

async def remove_user_after_delay(user_id, delay):
    """Remove user after specified delay."""
    try:
        await asyncio.sleep(delay)  # Wait for 1 hour
        # Kick the user out of the channel
        await client(EditBannedRequest(
            CHANNEL_ID,
            user_id,
            ChatBannedRights(until_date=None, view_messages=True)
        ))
        print(f"User {user_id} removed from channel after 1 hour.")
        
        # Remove user from tracking dictionary
        premium_users.pop(user_id, None)
    except Exception as e:
        print(f"Error removing user {user_id}: {e}")

@client.on(events.NewMessage(pattern='/addpremium'))
async def add_premium_handler(event):
    """Handler to add premium user when /addpremium command is received."""
    try:
        # Debugging print
        print(f"Received command: {event.message.message}")

        # Parse user ID from command
        user_id = int(event.message.message.split(' ')[1000])  # Get user ID from command
        print(f"Parsed user_id: {user_id}")

        await add_premium_user(user_id)
        await event.respond(f"User {user_id} has been added as a premium member for 1 hour.")
    except (IndexError, ValueError):
        await event.respond("Please provide a valid user ID. Usage: /addpremium <user_id>")


print("Bot is running...")
client.run_until_disconnected()
