from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm, BaseUserCreationForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError

from accounts.models import Profile
from accounts.utils import send_verify_mail

User = get_user_model()


class MyAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()

            if self.user_cache.is_verified == False:
                send_verify_mail(self.request, self.user_cache)
                raise ValidationError(
                    f"Email has not been verified.Please check your email.",
                    code="invalid_login"
                )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs.update({'class': 'form-control'})


class RegistrationForm(BaseUserCreationForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "class": "form-control"}, ),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs.update({'class': 'form-control'})


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs.update({'class': 'form-control'})


class ProfileEditForm(forms.ModelForm):
    bio = forms.CharField(required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs.update({'class': 'form-control'})


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email",
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "class": "form-control"}, ),
    )

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        if  User.objects.filter(email__iexact=self.cleaned_data['email']):
            return self.cleaned_data['email']
        else:
            raise ValidationError('There is no user with this email address')



class MySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs.update({'class': 'form-control'})


class MyPasswordChangeForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs.update({'class': 'form-control'})
