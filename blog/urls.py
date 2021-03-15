from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [

    path('', BlogListingsView.as_view(), name='blog-listing'),
    path('detail/<int:pk>/', BlogListingDetail.as_view(), name='blog-detail'),
    path('category-detail/<int:pk>/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('create/', CreateBlogView.as_view(), name='create-blog')

]