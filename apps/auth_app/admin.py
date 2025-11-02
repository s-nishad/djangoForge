from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, UserRole


# ---------------------
# User Creation Form
# ---------------------
class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all required
    fields, plus repeated password.
    """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "name", "phone_number", "profile_picture", "role")

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# ---------------------
# User Change Form
# ---------------------
class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all fields on
    the user, but replaces the password field with admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"))

    class Meta:
        model = User
        fields = ("email", "password", "name", "phone_number", "profile_picture", "role", "is_active", "is_staff", "is_superuser")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        return self.initial["password"]


# ---------------------
# Custom User Admin
# ---------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("email", "name", "role", "is_staff", "is_superuser", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "role")
    search_fields = ("email", "name", "phone_number")
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name", "phone_number", "profile_picture", "role")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "phone_number", "profile_picture", "role", "password1", "password2", "is_active", "is_staff", "is_superuser"),
            },
        ),
    )
