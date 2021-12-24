from django.urls import path
from accounts.api.views import register_user, login_user, logout_user, ChangePasswordView, user_profile_view

app_name = 'account'

urlpatterns = [
     path('register/', register_user, name="register"),
     path('login/', login_user, name="login"),
     path('logout/', logout_user, name="logout"),
     path('change-password/', ChangePasswordView.as_view(), name='change-password'),
     path('users/current/', user_profile_view, name='current_user'),
     path('users/current/profile_edit', user_profile_view, name='current_user_edit')
]