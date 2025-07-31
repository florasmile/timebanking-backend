from django.urls import path
from .views import UserProfileView, RegisterView, LogoutView, ChangePasswordView, EmailTokenLoginView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', EmailTokenLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name="change-password"),
]