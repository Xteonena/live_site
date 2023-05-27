from django.db import models
from django.contrib.auth.models import User


class PropertyType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Property(models.Model):
    title = models.CharField(max_length=100)
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    area = models.DecimalField(max_digits=8, decimal_places=2)
    rooms = models.IntegerField()
    floors = models.IntegerField()
    location = models.CharField(max_length=250)
    description = models.TextField()
    contact_info = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="property_images")


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}: {self.comment}"


class Chat(models.Model):
    users = models.ManyToManyField(User, related_name="chats")


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
