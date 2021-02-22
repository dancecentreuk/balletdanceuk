from django.db import models
from django.conf import settings
from pages.choices import day_choices, course_level_choices, location_choices, age_choices
from django.template.defaultfilters import slugify

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(default=None, editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def categories_count(self):
        return self.categories.all().count()+500

    def categories_count_listings(self):
        return self.categories.filter(is_posting=True).count()+500

    def categories_count_postings(self):
        return self.categories.filter(is_posting=False).count()+500




class Listing(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    location = models.CharField(max_length=100,
                                blank=False,
                                default=None,
                                choices=location_choices)
    date = models.DateField(null=True, blank=True)
    start_time = models.CharField(null=True, blank=True, max_length=10)
    end_time = models.CharField(null=True, blank=True, max_length=10)

    rehearsal_date = models.CharField(max_length=250, blank=True)
    fee = models.CharField(max_length=200)
    publish_date = models.DateTimeField(auto_now_add=True)
    is_posting = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)
    is_allowed = models.BooleanField(default=True)
    listing_image = models.ImageField(upload_to='listing_image/%Y/%m/%d', default='dance_class.jpg')
    slug = models.SlugField(max_length=100, default=None, editable=False)

    def __str__(self):
        return f'{self.id}-{self.title} by {self.author}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Listing, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']

