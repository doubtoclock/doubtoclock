from django.db import models
from django.contrib.auth.models import User

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