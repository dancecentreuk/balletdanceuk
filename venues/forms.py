from django import forms
from .models import *

class AddVenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'category', 'address', 'postcode','location', 'contact', 'contact_email', 'contact_mobile',
                  'mirrors', 'wooden_floor', 'music_system', 'floor_type', 'cost', 'venue_image', 'venue_image_1', 'venue_image_2']



class UpdateVenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'category', 'address', 'postcode','location', 'contact', 'contact_email', 'contact_mobile',
                  'mirrors', 'wooden_floor', 'music_system', 'floor_type', 'cost', 'venue_image', 'venue_image_1', 'venue_image_2']

