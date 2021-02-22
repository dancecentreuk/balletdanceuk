from django.contrib import admin
from .models import Conversation, Communication


admin.site.register(Communication)
admin.site.register(Conversation)

