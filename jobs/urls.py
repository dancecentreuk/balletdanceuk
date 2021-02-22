from django.urls import path
from .views import *

app_name = 'jobs'

urlpatterns = [
    path('listings/', ListingView.as_view(), name='jobs'),
    path('create-listing/', CreateListingView.as_view(), name='create-listing'),
    path('detail/<slug:slug>/<int:pk>/', SingleListingView.as_view(), name='single-listing'),
    path('update-listing/<slug:slug>/<int:pk>/', UpdateListingView.as_view(), name='update-listing'),
    path('delete/<slug:slug>/<int:pk>/', DeleteListingView.as_view(), name='delete-listing'),
    path('category-detail/listings/<slug:slug>/<int:pk>/', CategoryListingsView.as_view(), name='category-listings'),
    path('category-detail/postings/<slug:slug>/<int:pk>/', CategoryPostingsView.as_view(), name='category-postings'),
    path('search/listings/', search, name='search-listings'),
    path('search/postings/', searchPosting, name='search-postings'),
    path('postings/', PostingView.as_view(), name='postings'),
    path('create-posting', CreatePostingView.as_view(), name='create-posting'),
    path('post-detail/<slug:slug>/<int:pk>/', SinglePostingView.as_view(), name='single-posting'),
    path('update-posting/<slug:slug>/<int:pk>/', UpdatePostingView.as_view(), name='update-posting'),


]