from uuid import uuid4

from PIL import Image
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Group(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(User)
    invited_users = models.ManyToManyField(User, related_name='group_invitations', blank=True)
    chat_avatar = models.ImageField(default='default.png', upload_to='chat_images')
    exited_users = models.ManyToManyField(User, related_name='group_exited', blank=True)

    def __str__(self) -> str:
        return f"Group {self.name}-{self.uuid}"

    def get_absolute_url(self):
        return reverse("group", args=[str(self.uuid)])

    def invite_user(self, user):
        self.invited_users.add(user)
        self.save()

    def add_user_to_group(self, user: User):
        self.members.add(user)
        self.event_set.create(type="Join", user=user)
        self.save()

    def remove_user_from_group(self, user: User):
        self.members.remove(user)
        self.event_set.create(type="Left", user=user)
        self.save()

    def get_last_message(self):
        return self.message_set.order_by('-timestamp').first()

    def unread_messages_count(self, user):
        return self.message_set.exclude(users_read=user).exclude(author=user).count()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.chat_avatar:
            try:
                img = Image.open(self.chat_avatar.path)
                print(f"Image opened: {img.format}, {img.size}, {img.mode}")
                if img.height > 70 or img.width > 70:
                    new_img = (70, 70)
                    img.thumbnail(new_img)
                    img.save(self.chat_avatar.path)
                    print("Image saved successfully")
            except Exception as e:
                print(f"Error processing image: {e}")


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    users_read = models.ManyToManyField(User, related_name='read_messages', blank=True)

    def __str__(self) -> str:
        date = self.timestamp.date()
        time = self.timestamp.time()
        return f"{self.author} {date.month}.{date.day} {str(time)[:5]}\t{self.content}"


class Event(models.Model):
    CHOICES = [
        ("Join", "join"),
        ("Left", "left")
    ]
    type = models.CharField(choices=CHOICES, max_length=10)
    description = models.CharField(help_text="A description of the event that occurred", \
                                   max_length=50, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.description = f"{self.user} {self.type} the {self.group.name} group"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.description}"
