from django.urls import path
from .views import *

app_name ='pages'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('talent/', TalentListView.as_view(), name='talent'),
    path('talent/<int:pk>/<slug:slug>', TalentDetailView.as_view(), name='talent-detail'),
    path('profile-info/<int:pk>/<slug:first_name>/', ProfileInfoView.as_view(), name='profile-info'),
    path('search/talent/', searchTalent, name='search-talent'),



]
