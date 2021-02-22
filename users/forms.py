from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ChoiceField, DateInput

from pages.choices import account_type_choice, location_choices, gender_choices
from .models import Account, Profile, DancersProfile, CompanyProfile, DancerImage


class AccountRegisterForm(UserCreationForm):
    user_types = forms.CharField(label='User Type',
                                 widget=forms.RadioSelect(choices=account_type_choice))

    first_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form_firstname'}))

    last_name = forms.CharField(
        label='Lastname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Lastname', 'id': 'form-lastname'}))

    email = forms.EmailField(
        max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}
        )
    )

    location = forms.CharField(label='Location',
                               widget=forms.Select(choices=location_choices,
                                   attrs={'class': 'form-control mb-3', 'placeholder': 'Location', 'id': 'location'}
                               )
                               )

    gender = forms.CharField(label='Gender',
                               widget=forms.Select(choices=gender_choices,
                                                   attrs={'class': 'form-control mb-3',
                                                          'id': 'gender'}
                                                   )
                               )

    date_of_birth = forms.DateField(
         widget=forms.DateInput(
            attrs={'class': 'form-control mb-3',  'type': 'date', 'id': 'date_of_birth'}
        )
    )





    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']




class AccountProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['date_of_birth', 'mobile', 'location']



class UserUpdateForm(forms.ModelForm):



    class Meta:
        model = Profile
        fields = ['profile_image', 'date_of_birth', 'mobile', 'location' ]

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class DancersUpdateForm(forms.ModelForm):

    class Meta:
        model = DancersProfile
        fields = [ 'bio', 'experience', 'dancers_image', 'credits']

        widgets = {
        }


class CompanyUpdateForm(forms.ModelForm):

    class Meta:
        model = CompanyProfile
        fields = [ 'company_image', 'company_name', 'company_email', 'company_mobile', 'company_bio', 'is_active']

        widgets = {
        }


class DancerImageForm(forms.ModelForm):
    class Meta:
        model = DancerImage
        fields = ['title', 'image']


