from django.db import models
from django.contrib.auth.models import AbstractUser
import random
# Create your models here.

def get_default_pic():
    return f"profile/{random.choice(['p1.png','p2.png','p3.png','p4.png'])}"

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='profile/',default= get_default_pic, blank=True ,null= True)