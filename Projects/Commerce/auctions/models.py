from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_title = models.CharField(max_length=64)
    
    def __str__(self):
        return self.category_title

class Listing(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    price = models.PositiveIntegerField()
    image_url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")
    current_bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidder")
    
    def __str__(self):
        return self.name

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="comment_listing")
    text = models.CharField(max_length=150)
    
    def __str__(self):
        return f"{self.author}: {self.text} on {self.listing}"
    