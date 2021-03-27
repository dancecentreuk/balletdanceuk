from django.urls import path
from .views import *

app_name = 'mail'

urlpatterns = [
    path('inbox/', inbox, name='inbox'),
    path('inbox-new/', inbox_2, name='inbox'),
    path('outbox/', outbox, name='outbox'),
    path('create-communication/<int:pk>/', CreateCommunication.as_view(), name='create-communication'),
    path('create-communication-job/<int:pk>/', CreateCommunicationJob.as_view(), name='create-communication-job'),
    path('create-communication-venue/<int:pk>/', CreateCommunicationVenue.as_view(), name='create-communication-venue'),
    path('create-course-communication/<int:pk>/<int:course_id>/', CreateCourseCommunication.as_view(), name='create-course-communication'),
    path('create-talent-communication/<int:pk>/', CreateTalentCommunication.as_view(), name='create-talent-communication'),

    path('communication/<int:pk>/', communication_detail, name='communication'),
    path('delete-conversation/<int:pk>/', hide_conversation, name='delete-conversation'),
    # path('delete-conversation/<int:pk>/', HideConversationView.as_view(), name='delete-conversation'),



]