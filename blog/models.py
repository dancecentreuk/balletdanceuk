# from django.db import models
#
# # Create your models here.
#
# class Post(models.Model):
#     title = models.CharField(max_length=250)
#     description = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
#     location = models.CharField(max_length=100,
#                                 blank=False,
#                                 default=None,
#                                 choices=location_choices)
#     date = models.DateField(null=True, blank=True)
#     start_time = models.CharField(null=True, blank=True, max_length=10)
#     end_time = models.CharField(null=True, blank=True, max_length=10)
#
#     rehearsal_date = models.CharField(max_length=250, blank=True)
#     fee = models.CharField(max_length=200)
#     publish_date = models.DateTimeField(auto_now_add=True)
#     is_posting = models.BooleanField(default=True)
#     is_published = models.BooleanField(default=True)
#     is_allowed = models.BooleanField(default=True)
#     listing_image = models.ImageField(upload_to='listing_image/%Y/%m/%d', default='dance_class.jpg')
#     slug = models.SlugField(max_length=100, default=None, editable=False)
#
#     def __str__(self):
#         return f'{self.id}-{self.title} by {self.author}'
#
#     def save(self, *args, **kwargs):
#         self.slug = slugify(self.title)
#         super(Listing, self).save(*args, **kwargs)
#
#     class Meta:
#         ordering = ['-id']

