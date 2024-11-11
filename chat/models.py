from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    is_group = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    bio = models.TextField(max_length=500, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
    
    def get_avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/static/images/default-avatar.png'

# Signals pour créer automatiquement un profil utilisateur
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'userprofile'):
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
