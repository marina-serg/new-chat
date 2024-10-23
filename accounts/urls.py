from django.contrib.auth import views as auth_views
from django.urls import path

from .views import CustomPasswordResetView
from .views import SignUpView, login_user, profile, ChangePasswordView, profile_view

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('login/', login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('my-profile/', profile_view, name='my-profile'),
    path('profile/', profile, name='users-profile'),
    path('password_change/', ChangePasswordView.as_view(), name='password_change'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
