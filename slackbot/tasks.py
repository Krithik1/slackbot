from datetime import date
from slack_sdk import WebClient
from django.conf import settings
from .models import KitchenItem

client = WebClient(token=settings.SLACK_BOT_TOKEN)

def send_expiration_reminders():
    today = date.today()
    items = KitchenItem.objects.filter(expiration_date__lte=today)
    
    if items:
        item_list = "\n".join([f"{item.name} - {item.expiration_date}" for item in items])
        client.chat_postMessage(channel="#slack-bot", text=f"Expiring Soon:\n{item_list}")
