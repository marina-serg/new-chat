from django.contrib import admin

from .forms import RegistrationForm
from .models import User, Profile

class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    list_display = ("username", "email", "first_name", "last_name", "is_staff", 'is_verified')
    form = RegistrationForm
    inlines = [ProfileInline]


admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'bio')
    search_fields = ('user__email', 'user__username')
