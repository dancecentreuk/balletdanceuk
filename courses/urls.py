from django.urls import path
from .views import *

app_name = 'courses'

urlpatterns = [

    path('', CoursesView.as_view(), name='courses'),
    path('create/', CreateCourseView.as_view(), name='create-course'),
    path('detail/<int:pk>/<slug:slug>/', SingleCourseView.as_view(), name='course-detail'),
    path('update/<int:pk>/<slug:slug>/', UpdateCourseView.as_view(), name='update-course'),
    path('search/', searchCourse, name='search-course'),

]