from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', include('pages.urls')),
    path('courses/', include('courses.urls')),
    path('jobs/', include('jobs.urls')),
    path('new-mail/', include('mail.urls')),
    path('venues/', include('venues.urls')),
    path('blog/', include('blog.urls')),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
