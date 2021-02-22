from django.urls import path
from .views import *

app_name ='pages'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('talent/', TalentListView.as_view(), name='talent'),
    path('talent/<int:pk>/<slug:slug>', TalentDetailView.as_view(), name='talent-detail'),
    path('search/talent/', searchTalent, name='search-talent'),



]
