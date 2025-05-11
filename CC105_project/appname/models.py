from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    annual_income = models.FloatField()
    family_members = models.IntegerField()
    chronic_diseases = models.BooleanField()
    frequent_flyer = models.BooleanField()
    ever_travelled_abroad = models.BooleanField()
    employment_type_government_sector = models.BooleanField()
    employment_type_private_sector_or_self_employed = models.BooleanField()
    graduate_or_not = models.BooleanField()
    age = models.IntegerField()
    prediction = models.BooleanField()  
    probability = models.FloatField()
    prediction_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction for user {self.user.username if self.user else 'Guest'} at {self.prediction_timestamp.strftime('%Y-%m-%d %H:%M:%S')}"