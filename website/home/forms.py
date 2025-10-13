from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import UserImage, Doubt_jn, Doubt_fy

class CustomUserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("This email is already registered.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_active = False  # 🚨 important: disable login until verified
        if commit:
            user.save()
        return user


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['title', 'image']


class DoubtForm_jn(forms.ModelForm):
    class Meta:
        model = Doubt_jn
        fields = ['text']


class DoubtForm_fy(forms.ModelForm):
    class Meta:
        model = Doubt_fy
        fields = ['text']
