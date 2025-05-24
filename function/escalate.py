import functions_framework
import json
import os
import discord
import asyncio


def send_discord_message(message_content, channel_id, bot_token):
    class MyClient(discord.Client):
        async def on_ready(self):
            print(f'Logged in as {self.user} (ID: {self.user.id})')
            channel = self.get_channel(channel_id)
            if channel:
                await channel.send(message_content) 
                print("Message sent!")
            else:
                print("Could not find the channel.")
            await self.close()

    intents = discord.Intents.default()
    client = MyClient(intents=intents)
    client.run(bot_token)

def escalation_notify(request):
    urlparam = request.args.get('resourceid')
    bot_token = os.environ['BOT_TOKEN']
    channel_id = os.environ['CHANNEL_ID']
    message_content = f"The instance with resource-id {urlparam} was stopped"
    result = send_discord_message(message_content, channel_id, bot_token)
    return result, 200

















