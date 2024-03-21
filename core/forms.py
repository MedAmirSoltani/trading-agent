# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Preferences

class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name', 'email', 'birth_date', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        


class CustomUserChangeForm(forms.ModelForm):
    birth_date = forms.DateField(required=False)
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'birth_date']



class PreferencesForm(forms.ModelForm):
    class Meta:
        model = Preferences
        fields = ['risk_tolerance', 'investment_horizon', 'liquidity_needs', 'investment_objective', 'knowledge_experience', 'sectors', 'available_funds']
