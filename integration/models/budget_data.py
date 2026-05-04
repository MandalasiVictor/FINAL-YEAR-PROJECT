from django.utils import timezone
from django.db import models

class UserInputs(models.Model):
    total_budget = models.FloatField()  # Changed from DecimalField to FloatField
    campaign_type = models.CharField(max_length=50)
    target_audience = models.CharField(max_length=50)
    seasonality = models.CharField(max_length=50)
    preferred_channels = models.CharField(max_length=200)  # Comma-separated
    primary_interest = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.campaign_type} - {self.total_budget}"


class ModelOutputs(models.Model):
    user_input = models.ForeignKey(UserInputs, on_delete=models.CASCADE)
    optimal_budget_allocation = models.TextField()  
    expected_leads = models.IntegerField()
    estimated_revenue = models.FloatField()
    channel_effectiveness = models.TextField(default='{}')
    most_effective_channel = models.JSONField(default=dict)
    estimated_channel_revenue = models.TextField(default='{}')
    created_at = models.DateTimeField(default=timezone.now)
      

    def __str__(self):
        return f"Outputs for {self.user_input}"
    
