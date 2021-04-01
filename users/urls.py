from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('update/<int:pk>', UserUpdateView.as_view(), name='update-profile'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('create_dancers_profile/', CreateDancerProfileView.as_view(), name='create-dancers-profile'),
    path('delete-dancers-profile/<int:pk>/', DeleteDancersProfile.as_view(), name='delete-dancers-profile'),
    path('create_company_profile/', CreateCompanyProfileView.as_view(), name='create-company-profile'),
    path('delete-company-profile/<int:pk>/', DeleteCompanyProfile.as_view(), name='delete-company-profile'),
    path('delete-photo/<int:pk>/', delete_dancer_photo, name='delete-dancers-photo'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate')


]