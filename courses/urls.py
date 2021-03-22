from django.urls import path
from .views import *

app_name = 'courses'

urlpatterns = [

    path('', CoursesView.as_view(), name='courses'),
    path('create/', CreateCourseView.as_view(), name='create-course'),
    path('level/<int:pk>/<slug:slug>/', CourseLevelDetailView.as_view(), name='level_detail'),
    path('detail/<int:pk>/<slug:slug>/', SingleCourseView.as_view(), name='course-detail'),
    path('update/<int:pk>/<slug:slug>/', UpdateCourseView.as_view(), name='update-course'),
    path('search/', searchCourse, name='search-course'),
    path('create-review/<int:pk>/', CreateCourseReview.as_view(), name='create-review'),
    path('update-review/<int:pk>/', UpdateCourseReview.as_view(), name='update-review'),

]