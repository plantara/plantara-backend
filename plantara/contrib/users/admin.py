from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from plantara.admin import admin_site

from . import forms, models


class UserAdmin(BaseUserAdmin):
    form = forms.CustomUserChangeForm
    add_form = forms.CustomUserCreationForm
    add_form_template = "users/admin_form.html"
    list_display = ("email", "first_name", "last_name", "is_staff")
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


admin_site.register(models.User, UserAdmin)
