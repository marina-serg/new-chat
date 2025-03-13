from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=150, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "account"
        verbose_name_plural = "accounts"

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.png', upload_to='profile_images')
    bio = models.TextField()

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)

    def __str__(self):
        return self.user.email
