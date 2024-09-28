#!/user/bin/env python
# -*- coding: utf-8 -*-

import json
import discord
import asyncio

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

authcode = None  # Store authcode globally for use outside of the event


async def run(token):
    try:
        await client.start(token)  # Start the bot
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Ensure we close the aiohttp session properly after stopping the client
        await client.close()  # Clean up the client session


@client.event
async def on_ready():
    print(f"目前登入身份 --> {client.user}")


@client.event
async def on_message(message):
    global authcode  # Modify global variable
    # 排除機器人本身的訊息，避免無限循環
    if message.author == client.user:
        return
    if client.user.mentioned_in(message):
        authcode = message.content.replace(f"<@{client.user.id}> ", "").strip()
        await message.reply("收到，驗證中!")
        await client.close()  # Close the connection after getting the authcode


def start_bot():
    with open('config.json', 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)
    
    token = config["discord"][0]["token"]
    
    # Start the Discord client asynchronously
    asyncio.run(run(token))
    
    # After the client is closed, return the authcode
    return authcode

