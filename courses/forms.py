import form as form
from django import forms
from .models import *

class CreateCoursesForm(forms.ModelForm):
    class Meta:
        model = WeeklyBalletClass
        fields = ['title', 'location', 'course_level', 'age_group', 'day', 'start_time', 'end_time', 'address',
                  'postcode', 'price', 'teacher', 'faq', 'clothes', 'experience', 'average_age', 'drop_in',
                  'about_dance_class', 'dance_class_image', 'dance_class_image_1', 'dance_class_image_2', 'dance_class_image_3']







class UpdateCourseForm(forms.ModelForm):
    class Meta:
        model = WeeklyBalletClass
        fields = ['title', 'location', 'course_level', 'age_group', 'day', 'start_time', 'end_time', 'address',
                  'postcode', 'price', 'teacher', 'faq', 'clothes', 'experience', 'average_age', 'drop_in',
                  'about_dance_class', 'dance_class_image', 'dance_class_image_1', 'dance_class_image_2', 'dance_class_image_3']




class CourseReviewForm(forms.ModelForm):
    class Meta:
        model = CourseReview
        fields = ['comment', 'rating']

        labels = {
            'comment': ('Review'),
            'rating': ('Rating out of 10'),
        }

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'label': 'review'}),
            'rating': forms.TextInput(attrs={ 'type':'range', 'id' :'rangeInput',
                                             'min':'0', 'max':'10', 'step':'0.5', 'oninput': 'amount.value=rangeInput.value',
                                             }),

        }






