import os
import requests
import functions_framework  # GCP Functions Framework

import asyncio
from google.cloud import compute

import datetime

# test for cloud build trigger
# redeploy pls

async def stop_instance(project_id, zone, instance_name):
    """Stops a Compute Engine instance."""
    instances_client = compute.InstancesClient()
    try:
        request = compute.StopInstanceRequest()
        request.project = project_id
        request.zone = zone
        request.instance = instance_name

        operation = instances_client.stop(request=request)
        print(f"Stopping instance {instance_name}...")

        # Wait for the operation to complete (optional but recommended)
        try:
            operation.result()  # Wait synchronously
            print(f"Instance {instance_name} stopped successfully.")
            return True
        except Exception as e:
            print(f"Error waiting for operation: {e}")
            return False

    except Exception as e:
        print(f"Error stopping instance: {e}")
        return False


def send_discord(request):
    urlparam = request.args.get('resourceid')
    bot_token = os.environ['BOT_TOKEN']
    channel_id_string = os.environ['CHANNEL_ID']
    channel_id = int(channel_id_string)
    message_content = f"The instance with resource-id {urlparam} was stopped at {datetime.datetime.now()}, because of an escalation."

    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

    Headers = {"Authorization": f"Bot {bot_token}", "User-Agent": "DiscordBot (sims, v0.1)"}

    payload = {
        "content": message_content
    }

    response = requests.post(url, payload, headers=Headers, timeout=5)
    response.raise_for_status()


@functions_framework.http
def escalation_notify(request):
    instance_name = request.args.get('resourceid')
    zone = request.args.get('zone')
    project_id = "os-ccs"

    stopping_result = asyncio.run(stop_instance(project_id, zone, instance_name))

    if stopping_result:
        send_discord(request)
        return 'done'
    else:
        return 'error'
