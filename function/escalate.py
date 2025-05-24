import requests
    import json
    import os

    def send_discord_message(message_content, channel_id, bot_token):
        """Sends a message to a Discord channel."""
        headers = {
            "Authorization": f"Bot {bot_token}"
        }
        data = {
            "content": message_content
        }
        url = f"https://discord.com/api/channels/%7Bchannel_id%7D/messages"
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return "Message sent successfully!"
        else:
            return f"Failed to send message. Status code: {response.status_code}"

    # Your main function (e.g., called by an HTTP request)
    def escalation_notify(request):
        # Replace with your bot token and the Discord channel ID
        
        bot_token = os.environ['BOT_TOKEN']
        channel_id = os.environ['CHANNEL_ID']
        message_content = "This message is from a Cloud Function!"

        # Call the function to send the message
        result = send_discord_message(message_content, channel_id, bot_token)

        # Return a response to the user (or log it)
        return result, 200

















