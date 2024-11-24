from django.db import models
from django.contrib.auth.models import User

class Calibri(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Name")
    RR = models.CharField(max_length=255, verbose_name="RR")
    stress_num = models.CharField(max_length=255, verbose_name="Stress Number")
    stress_level = models.CharField(max_length=255, verbose_name="Stress Level")
    owner = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='calibri_devices', null=True, blank=True)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    colibri_login = models.CharField(max_length=100, blank=True, null=True)
    colibri_password = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"