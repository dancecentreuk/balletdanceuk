from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from .models import *
from jobs.models import Listing
from .forms import CreateCommunicationForm,  HideConversationForm
from users.models import Account, DancersProfile
from django.db.models import Q

# Create your views here.
from django.views.generic import CreateView, UpdateView
from django.db.models import Count, Min, Max, Avg, OuterRef
from django.db.models import Subquery, Max, F



def inbox(request):
    communications = Communication.objects.filter(recipient=request.user).distinct()
    unread_messages = communications.filter(read_at=None).count()





    context = {
        'communications': communications,
        'unread_messages': unread_messages
    }
    return render(request, 'mail/inbox.html', context)



def inbox_2(request):
    conversations = Conversation.objects.filter(conversations__recipient=request.user).order_by('-updated').distinct()
    for conversation in conversations:
        if request.user == conversation.messenger_1:
            conversations = conversations.filter(messenger_1_hidden=False)
        else:
            conversations = conversations.filter(messenger_2_hidden=False)


    context = {
        'conversations': conversations,
        # 'new_chats' : new_chats
    }
    return render(request, 'mail/inbox_2.html', context)

def outbox(request):
    conversations = Conversation.objects.filter(conversations__sender=request.user).order_by('-updated').distinct()
    for conversation in conversations:
        if request.user == conversation.messenger_1:
            conversations = conversations.filter(messenger_1_hidden=False)
        else:
            conversations = conversations.filter(messenger_2_hidden=False)


    context = {
        'conversations': conversations,
        # 'new_chats' : new_chats
    }
    return render(request, 'mail/outbox.html', context)


def communication_detail(request, pk):


    inbox_count = Communication.objects.filter(recipient=request.user).filter(read_at=None).count()
    conversation = get_object_or_404(Conversation, id=pk)
    all_communication = Communication.objects.filter(conversation_id = conversation)\
        .filter(Q(recipient=request.user) & Q(recipient_hidden=False) | Q(sender=request.user) & Q(sender_hidden=False))






    user = request.user
    now = timezone.now()
    new_timestamp = timezone.now()
    messenger1 = conversation.messenger_1




    if request.method == 'POST':
        sender = user
        recipient = request.POST['recipient']
        content = request.POST['content']
        conversation = request.POST['conversation']
        recipient = Account.objects.get(id=recipient)

        communication = Communication(content=content,
                                      sender=sender,
                                      recipient=recipient,
                                      conversation_id=conversation
                                      )

        if user == messenger1:
            Conversation.objects.filter(pk=conversation).update(messenger_1_updated=new_timestamp, updated=new_timestamp, messenger_2_hidden=False)
        else:
            Conversation.objects.filter(pk=conversation).update(messenger_2_updated=new_timestamp, updated=new_timestamp, messenger_1_hidden=False)

        communication.save()
        return redirect('mail:communication',  pk)


    context = {
        'all_convo': all_communication,
        'inbox_count': inbox_count,
        'conversation':conversation
    }
    return render(request, 'mail/communication.html', context)





class CreateCommunication(CreateView):
    model = Listing
    template_name = 'mail/create-communication.html'
    form_class = CreateCommunicationForm
    success_url = '/'



    def form_valid(self, form):
        listing = get_object_or_404(Listing, pk=self.kwargs['pk'])
        communication = form.save(commit=False)
        communication.sender = self.request.user
        communication.recipient = listing.author
        conversation = Conversation.objects.create(title=listing.title, messenger_1=communication.sender, messenger_2=communication.recipient)
        communication.conversation_id = conversation.id
        communication.save()
        return super(CreateCommunication, self).form_valid(form)


    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.request.user.id})


def hide_conversation(request, pk):

    conversation = Conversation.objects.get(id=pk)
    communications = Communication.objects.filter(conversation_id=pk)


    if request.user == conversation.messenger_2:
        pass
    elif request.user ==  conversation.messenger_1:
        pass
    else:
        return redirect('/')


    if request.method == 'POST':
        form = HideConversationForm(request.POST, instance=conversation)
        if request.user == conversation.messenger_1:
            if form.is_valid():
                data = form.save(commit=False)
                data.messenger_1_hidden=True
                data.save()

                for communication in communications:
                    if communication.recipient == request.user:
                        communication.recipient_hidden = True
                        communication.save()
                        if communication.recipient_hidden == True and communication.sender_hidden == True:
                            communication.delete()
                    if communication.sender == request.user:
                        communication.sender_hidden = True
                        communication.save()
                        if communication.recipient_hidden == True and communication.sender_hidden == True:
                            communication.delete()

                return redirect('mail:inbox')

        elif request.user == conversation.messenger_2:
            if form.is_valid():
                data = form.save(commit=False)
                data.messenger_2_hidden=True
                data.save()

                for communication in communications:
                    if communication.recipient==request.user:
                        communication.recipient_hidden = True
                        communication.save()
                        if communication.recipient_hidden == True and communication.sender_hidden == True:
                            communication.delete()
                    if communication.sender == request.user:
                        communication.sender_hidden = True
                        communication.save()
                        if communication.recipient_hidden == True and communication.sender_hidden == True:
                            communication.delete()

                return redirect('mail:inbox')
        else:
            return redirect('pages:home')
    else:
        form = HideConversationForm()

    context = {
        'form':form,
        'conversation':conversation

    }
    return render(request, 'mail/delete-conversation.html' , context)


class CreateTalentCommunication(CreateView):
    model = DancersProfile
    template_name = 'mail/create-communication.html'
    form_class = CreateCommunicationForm
    success_url = '/'



    def form_valid(self, form):
        talent = get_object_or_404(DancersProfile, pk=self.kwargs['pk'])
        communication = form.save(commit=False)
        communication.sender = self.request.user
        communication.recipient = talent.user
        title = 'Message from ' + self.request.user.first_name
        conversation = Conversation.objects.create(title=title, messenger_1=communication.sender, messenger_2=communication.recipient)
        communication.conversation_id = conversation.id
        communication.save()
        return super(CreateTalentCommunication, self).form_valid(form)


    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.request.user.id})


