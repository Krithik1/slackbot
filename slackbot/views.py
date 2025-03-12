from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import KitchenItem
from datetime import datetime
from slack_sdk import WebClient
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from slackbot.tasks import send_expiration_reminders


client = WebClient(token=settings.SLACK_BOT_TOKEN)

@csrf_exempt
def slack_command(request):
    if request.method == "POST":
        data = request.POST
        command = data.get("text", "").split()
        print(command)
        
        if len(command) == 3 and command[0].lower() == "add":
            item_name, expiry = command[1], command[2]
            try:
                expiry_date = datetime.strptime(expiry, "%Y-%m-%d").date()
                KitchenItem.objects.create(name=item_name, expiration_date=expiry_date)
                return JsonResponse({"text": f"Added {item_name}, expiring on {expiry}"})
            except ValueError:
                return JsonResponse({"text": "Invalid date format. Use YYYY-MM-DD."})

        elif command[0].lower() == "remove":
            item_name = command[1]
            deleted, _ = KitchenItem.objects.filter(name=item_name).delete()
            if deleted:
                return JsonResponse({"text": f"Removed {item_name}."})
            return JsonResponse({"text": f"{item_name} not found."})
        
        else:
            items = KitchenItem.objects.all()
            if not items:
                return JsonResponse({"text": "Your fridge is empty!"})
            item_list = "\n".join([f"{item.name} - {item.expiration_date}" for item in items])
            return JsonResponse({"text": f"Fridge Items:\n{item_list}"})

    return JsonResponse({"text": "Invalid command. Use `/add item YYYY-MM-DD`, `/list`, or `/remove item`."})

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_expiration_reminders, 'interval', hours=24)
    scheduler.start()

start_scheduler()