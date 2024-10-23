from django import forms

from .models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'chat_avatar']


class InviteUserForm(forms.Form):
    email = forms.EmailField(label='Email пользователя для приглашения')
