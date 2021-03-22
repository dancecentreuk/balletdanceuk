from django.contrib import admin
from .models import WeeklyBalletClass, Level, CourseReview

# Register your models here.
admin.site.register(WeeklyBalletClass)
admin.site.register(Level)
admin.site.register(CourseReview)