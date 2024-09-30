#!/user/bin/env python
# -*- coding: utf-8 -*-
import discord
import asyncio
import time

class UserAccountBot:
    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        self.OTPresults = {}  # Store OTPs for multiple user accounts
        self.pending_accounts = {}  # Keep track of accounts waiting for OTPs

        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)

        # Register event handlers
        self.client.event(self.on_ready)
        self.client.event(self.on_message)

    async def run(self):
        try:
            await self.client.start(self.token)  # Start the bot
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await self.client.close()

    def start(self):
        # Use asyncio to run the bot
        asyncio.run(self.run())

    async def on_ready(self):
        print(f"Bot logged in as {self.client.user}")
        for account in self.pending_accounts:
            await self.send_welcome_message(account)

    async def send_welcome_message(self, account):
        # Send a welcome message to the Discord channel for the account
        await self.client.get_channel(self.channel_id).send(f"{account} 訂票成功，請輸入驗證碼")

    async def on_message(self, message):
        if message.author == self.client.user:
            return  # Ignore messages from the bot itself

        for account in self.pending_accounts:
            if self.client.user.mentioned_in(message):
                # Extract and store the authcode for the specific account
                authcode = message.content.replace(f"<@{self.client.user.id}> ", "").strip()
                self.OTPresults[account] = authcode
                await message.reply(f"{account} 收到，驗證中!")
                self.pending_accounts.pop(account)  # Remove the account from pending after receiving OTP
                if not self.pending_accounts:  # Close the bot if no more accounts pending
                    await self.client.close()
                break

    def add_account(self, account):
        """Adds a user account to pending accounts."""
        self.pending_accounts[account] = True

    def get_authcode(self, account):
        """Waits for OTP and returns authcode for the account."""
        while account not in self.OTPresults:
            time.sleep(1)  # Wait until OTP is received
        return self.OTPresults[account]

    
