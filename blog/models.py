from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify



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



class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='categories')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    publish_date = models.DateTimeField(auto_now=False, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_posting = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    is_allowed = models.BooleanField(default=False)
    blog_image = models.ImageField(upload_to='blog_image/%Y/%m/%d', default='blog_image.jpg')
    slug = models.SlugField(max_length=100, default=None, editable=False)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id}-{self.title} by {self.author}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']




