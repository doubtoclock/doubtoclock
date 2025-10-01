from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserImage

class CustomUserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]  # ✅ store email
        if commit:
            user.save()
        return user


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UserImage
        fields = ['title', 'image']