from django.urls import path
from .views import *

app_name = 'venues'

urlpatterns = [
path('', VenuesView.as_view(), name='venues'),
path('add-venue/', AddVenueView.as_view(), name='add-venue'),


]