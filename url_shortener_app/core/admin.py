from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from django.core.exceptions import ValidationError
# Register your models here.


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('mobile_number',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match",)
        return password2

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get("mobile_number")
        if len(mobile_number) != 11 or mobile_number[0:2] != '09':
            raise ValueError('Invalid mobile number')
        return mobile_number

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'mobile_number',
            'email',
            'password',
            'is_active',
            'is_superuser',
            'is_staff',
            'user_permissions',
        )

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get("mobile_number")
        if len(mobile_number) != 11 or mobile_number[0:2] != '09':
            raise ValueError('Invalid mobile number')
        return mobile_number


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id', 'mobile_number', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('mobile_number', 'email', 'password',
                           'is_active',)}),
        ('User Types', {'fields': ('is_superuser', 'is_staff')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('mobile_number',)
    ordering = ('mobile_number',)
    filter_horizontal = ('user_permissions',)


admin.site.register(User, UserAdmin)
