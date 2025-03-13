from django import forms

from .models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name','chat_avatar' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.fields:
            self.fields[name].widget.attrs.update({'class': 'form-control'})


class InviteUserForm(forms.Form):
    email = forms.EmailField(label='Email for invite', widget=forms.EmailInput(attrs={'class': 'form-control'}))
