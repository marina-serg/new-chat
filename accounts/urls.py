from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
    path('register/', RegistrationView.as_view(), name='register'),
    path('password_verify_confirm/<uidb64>/<token>/', EmailVerify.as_view(), name='password_verify_confirm'),
    path('confirm_email/', TemplateView.as_view(template_name='registration/confirm_email.html',
                                                ), name='confirm_email'),
    path('edit/', EditView.as_view(), name='edit'),
    path('users/<username>/', UserDetailView.as_view(), name='user_detail'),
    path('password_change/', ChangePasswordView.as_view(), name='password_change'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
