from django.db import models
from django.conf import settings
from datetime import datetime

# Create your models here.
from django.urls import reverse
from django.db.models import Count, Min, Max, Avg



class Conversation(models.Model):
    title = models.CharField(max_length=250)
    updated = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    messenger_1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messenger_1', null=True, blank=True)
    messenger_2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messenger_2', null=True, blank=True)
    messenger_1_updated = models.DateTimeField(blank=True, null=True)
    messenger_2_updated = models.DateTimeField(blank=True, null=True)
    messenger_1_hidden = models.BooleanField(default=False)
    messenger_2_hidden = models.BooleanField(default=False)


    def __str__(self):
        return '{}'.format(self.id)

    def communications_message_1(self):
        return self.conversations.filter(sender=self.messenger_1).filter(recipient_hidden=False).order_by('id').last()



    def communications_message_2(self):
        return self.conversations.filter(sender=self.messenger_2).filter(recipient_hidden=False).order_by('id').last()



    def communications(self):
        return self.conversations.all().last()

    def undeleted_conversation(self):
        return self.conversations.filter()

    def inbox_exp(self):
        return self.conversations.filter(recipient=self.messenger_1)

    def get_absolute_url(self):
        return reverse('mail:communication', kwargs={'id': self.id})

    def get_last_message(self):
        return self.conversations.annotate(Min('timestamp')).last()

    def get_last_message_timestamp(self):
        message = Communication.objects.filter(conversation=self, sender=self.messenger_1).last()
        return message.timestamp if message else ""








class Communication(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now, blank=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipient')
    read_at = models.DateTimeField(null=True, blank=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.DO_NOTHING, related_name='conversations')
    sender_hidden = models.BooleanField(default=False)
    recipient_hidden = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return  f'conversation id : {self.conversation} sender : {self.sender} recipient = {self.recipient} deleted : {self.deleted}'

