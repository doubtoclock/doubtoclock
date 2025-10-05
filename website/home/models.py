from django.db import models
from django.contrib.auth.models import User
import random

class DoubtCoinWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.balance} Doubtcoins"


class UserImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="user_images/")  # goes to Cloudinary

    def __str__(self):
        return self.title


class Doubt_jn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doubts")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Doubt by {self.user.username} at {self.created_at}"    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    random_number = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Assign a random number between 1–8 only once (at creation)
        if not self.random_number:
            self.random_number = random.randint(1, 8)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.random_number}"