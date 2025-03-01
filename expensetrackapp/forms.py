from django import forms
from .models import UserProfile  # Adjust this based on your model

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'profile_picture', 'bio']  # Adjust based on your model fields
