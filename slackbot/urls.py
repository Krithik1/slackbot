from django.contrib import admin
from django.urls import path
from slackbot.views import slack_command

urlpatterns = [
    path('admin/', admin.site.urls),
    path('slack/', slack_command),
]
