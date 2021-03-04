from django.urls import path
from .views import *

app_name = 'venues'

urlpatterns = [
    path('', VenuesView.as_view(), name='venues'),
    path('add-venue/', AddVenueView.as_view(), name='add-venue'),
    path('detail/<int:pk>/', SingleVenueView.as_view(), name='venue-detail'),
    path('update/<int:pk>/', UpdateVenueView.as_view(), name='update-venue'),
    path('delete/<int:pk>/', DeleteVenueView.as_view(), name='delete-venue'),

]