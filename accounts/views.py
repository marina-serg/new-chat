import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView, PasswordResetConfirmView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, DetailView

from accounts.forms import MyAuthenticationForm, RegistrationForm, MyPasswordResetForm, MySetPasswordForm, \
    MyPasswordChangeForm
from accounts.utils import send_verify_mail
from .forms import UserEditForm, ProfileEditForm

LOGGER = logging.getLogger('accounts')

User = get_user_model()

from .tasks import send_reset_email


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')
    form_class = MyPasswordChangeForm


class CustomPasswordResetView(PasswordResetView):
    form_class = MyPasswordResetForm
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        response = super().form_valid(form)
        for user in form.get_users(email):
            send_reset_email.delay(subject='Password Reset',
                                   message='Follow this link to reset your password.',
                                   recipient_list=[user.email]
                                   )
        return response


class MyLoginView(LoginView):
    form_class = MyAuthenticationForm


class RegistrationView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            user = form.save()
            send_verify_mail(request, user)
            return redirect('confirm_email')
        else:
            return self.form_invalid(form)


class EmailVerify(View):
    token_generator = PasswordResetTokenGenerator()

    def dispatch(self, *args, **kwargs):
        self.user = self.get_user(kwargs["uidb64"])
        if self.user is not None:
            token = kwargs["token"]
            if self.token_generator.check_token(self.user, token):
                self.user.is_verified = True
                self.user.save()
                messages.success(self.request, 'Email Verified')
                return redirect('login')
            messages.error(self.request, 'Token invalid')
            return redirect('home')

    def get_user(self, uidb64):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        return user


class EditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {
            'user_form': UserEditForm(instance=request.user),
            'profile_form': ProfileEditForm(instance=request.user.profile),
        }
        return render(request, template_name='registration/edit.html', context=data)

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        else:
            messages.error(request, 'Your account could not be updated!')

        return render(request, template_name='registration/edit.html', context={
            'user_form': user_form,
            'profile_form': profile_form})


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'registration/users_detail.html'
    context_object_name = 'user'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_queryset(self):
        return User.objects.filter(is_active=True)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = MySetPasswordForm
