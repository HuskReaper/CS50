from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.db import models

class User(AbstractUser):
    pass
    
class Post(models.Model):
    paginate_by = 10
    id = models.BigAutoField(primary_key=True)
    content = models.TextField(blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    timestamp = models.DateTimeField(auto_now_add=True)
    is_liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    like_count = models.PositiveIntegerField(default=0)
    liked = models.BooleanField(default=False)
    
    def toggle_like(self, user):
        if user.is_authenticated:
            if user in self.is_liked_by.all():
                self.is_liked_by.remove(user)
                self.like_count -= 1
            else:
                self.is_liked_by.add(user)
                self.like_count += 1
        self.save()
    
    def serialize(self):
        return {
            'id': self.id,
            'author': self.author.username,
            'content': self.content,
            'timestamp': self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            'like_count': self.like_count,
            'liked': self.liked
        }

    def __str__(self):
        return f"{self.author}: {self.content}"
    
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    content = models.TextField(blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commenter") 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="commented_post")
    
    def __str__(self):
        return f"{self.author}: {self.content} on {self.post.author}'s post."
 
class Follow(models.Model):
    id = models.BigAutoField(primary_key=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="follower")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="followed")
    
    def __str__(self):
        return f"{self.follower} follows {self.followed}"
    
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(User)