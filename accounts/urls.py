from django.urls import path, include
from .views import DeleteUserView ,RegisterUserView, RegisterDoneView, PasswordChangeView, LoginView, profile, LogoutView, ChangeUserInfoView
app_name = 'accounts'

urlpatterns = [
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/delete', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/password/change/', PasswordChangeView.as_view(), name='password_change'),
]
