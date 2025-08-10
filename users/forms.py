from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
import re
from .models import CustomUser

User= get_user_model()
class CustomSignupForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        # model = User
        model = User
        fields = ['username','first_name','email','password1','password2']
        labels = {
            'first_name': 'Full Name'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        
        allowed_domains=['gmail.com','yahoo.com','outlook.com','github.com']
        pattern = r'^[\w\.-]+@([\w\.-]+)$'
        match = re.match(pattern,email) # returns an object if pattern matched

        if match:
            domain = match.group(1)
            if domain not in allowed_domains:
                raise forms.ValidationError("Please use a valid email from gmail,yahoo etc")
        
        else:
            raise forms.ValidationError("Invalid email format.")

        return email