from django import forms
from .models import *

class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'location', 'rehearsal_date', 'fee', 'listing_image']


class UpdateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'category', 'location', 'rehearsal_date', 'fee', 'listing_image']


class CreatePostingForm(forms.ModelForm):

    date = forms.CharField(max_length=20, widget=forms.DateInput(
        attrs={'class': 'form-control', 'type':'date', 'placeholder':'Enter Job Date'}
    ))
    start_time = forms.CharField(max_length=20, widget=forms.TimeInput(
        attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Enter Job Date'}
    ))
    end_time = forms.CharField(max_length=20, widget=forms.TimeInput(
        attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Enter Job Date'}
    ))

    class Meta:
        model = Listing
        fields = ['title', 'description',  'date', 'start_time', 'end_time', 'category', 'location', 'rehearsal_date', 'fee', 'listing_image']


class UpdatePostingForm(forms.ModelForm):

    date = forms.CharField(max_length=20, widget=forms.DateInput(
        attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Enter Job Date'}
    ))
    start_time = forms.CharField(max_length=20, widget=forms.TimeInput(
        attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Enter Job Date'}
    ))
    end_time = forms.CharField(max_length=20, widget=forms.TimeInput(
        attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Enter Job Date'}
    ))
    class Meta:
        model = Listing
        fields = ['title', 'description', 'date', 'start_time', 'end_time', 'category', 'location',
                  'rehearsal_date', 'fee', 'listing_image']