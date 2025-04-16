from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Set email as username
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='Current Password'
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='New Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        label='Confirm New Password'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        # Only validate passwords if the user is trying to change them
        if new_password or current_password or confirm_password:
            if not current_password:
                raise forms.ValidationError('Current password is required')
            if not new_password:
                raise forms.ValidationError('New password is required')
            if not confirm_password:
                raise forms.ValidationError('Password confirmation is required')
            if new_password != confirm_password:
                raise forms.ValidationError('New passwords do not match')
            if not self.instance.check_password(current_password):
                raise forms.ValidationError('Current password is incorrect')

        return cleaned_data





