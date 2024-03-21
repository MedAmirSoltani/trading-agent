# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    preferences = models.OneToOneField('Preferences', on_delete=models.CASCADE, null=True, blank=True)


class Preferences(models.Model):
    RISK_TOLERANCE_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    INVESTMENT_HORIZON_CHOICES = [
        ('short_term', 'Short Term'),
        ('medium_term', 'Medium Term'),
        ('long_term', 'Long Term')
    ]

    LIQUIDITY_NEEDS_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    INVESTMENT_OBJECTIVE_CHOICES = [
        ('capital_preservation', 'Capital Preservation'),
        ('income_generation', 'Income Generation'),
        ('wealth_accumulation', 'Wealth Accumulation')
    ]

    KNOWLEDGE_EXPERIENCE_CHOICES = [
        ('novice', 'Novice'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ]
    SECTORS_CHOICES = [
        ('banks', 'Banks'),
        ('leasing', 'Leasing'),
        ('others', 'Others'),
        ('all', 'All')
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_preferences')
    risk_tolerance = models.CharField(max_length=10, choices=RISK_TOLERANCE_CHOICES)
    investment_horizon = models.CharField(max_length=20, choices=INVESTMENT_HORIZON_CHOICES)
    liquidity_needs = models.CharField(max_length=10, choices=LIQUIDITY_NEEDS_CHOICES)
    investment_objective = models.CharField(max_length=20, choices=INVESTMENT_OBJECTIVE_CHOICES)
    knowledge_experience = models.CharField(max_length=20, choices=KNOWLEDGE_EXPERIENCE_CHOICES)
    sectors = models.CharField(max_length=20, choices=SECTORS_CHOICES)
    available_funds = models.DecimalField(max_digits=12, decimal_places=2)
