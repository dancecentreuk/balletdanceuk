from django.db import models
from django.conf import settings
from pages.choices import day_choices, course_level_choices, location_choices, age_choices
from django.template.defaultfilters import slugify
from django.utils import timezone

# Create your models here.

class Level(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(default=None, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Level, self).save(*args, **kwargs)

    def courses_count(self):
        return self.courses.all().count()+500




class WeeklyBalletClass(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    location = models.CharField(max_length=100,
                                blank=False,
                                default=None,
                                choices=location_choices)
    course_level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='courses')
    age_group = models.CharField(max_length=50,
                                 blank=False,
                                 default=None,
                                 choices=age_choices)
    day = models.CharField(max_length=20,
                           blank=False,
                           default=None,
                           choices=day_choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    address = models.CharField(max_length=350)
    postcode = models.CharField(max_length=15)
    price = models.FloatField()
    teacher = models.CharField(blank=True, max_length=100)
    faq = models.TextField()
    clothes = models.CharField(max_length=300, blank=True)
    experience = models.CharField(max_length=300, blank=True)
    average_age = models.CharField(max_length=300, blank=True)
    drop_in = models.CharField(max_length=300, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    about_dance_class = models.TextField()
    is_published = models.BooleanField(default=True)
    is_allowed = models.BooleanField(default=True)
    dance_class_image = models.ImageField(upload_to='dance_class_image/%Y/%m/%d', default='dance_class.jpg')
    dance_class_image_1 = models.ImageField(upload_to='dance_class_image/%Y/%m/%d', blank=True)
    dance_class_image_2 = models.ImageField(upload_to='dance_class_image/%Y/%m/%d', blank=True)
    dance_class_image_3 = models.ImageField(upload_to='dance_class_image/%Y/%m/%d', blank=True)
    slug = models.SlugField(default=None, editable=False)

    def __str__(self):
        return f'{self.id}-{self.title} by {self.author}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(WeeklyBalletClass, self).save(*args, **kwargs)

    def updated_info(self):
        if self.updated is None:
            return self.timestamp
        return self.updated

    def has_commented(self):
        return self.ballet_classes.all().values()



    class Meta:
        ordering = ['-id']


class CourseReview(models.Model):
    course = models.ForeignKey(WeeklyBalletClass, on_delete=models.CASCADE, related_name='ballet_classes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.user.first_name








