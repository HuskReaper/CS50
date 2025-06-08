from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post, Follow
import json

# LOADS #
def index(request):
    # Use pagination to create page objects.
    posts = Post.objects.all().order_by('-timestamp')
    page = Paginator(posts, 10)
    
    # Get page request and return corresponding page object.
    page_num = request.GET.get("page")
    page_obj = page.get_page(page_num)
    return render(request, "network/index.html", {'page_obj': page_obj})
    
def load_posts(request, view):
    if view == "all_posts":
        # Use pagination to create page objects.
        posts = Post.objects.all().order_by('-timestamp')
        page = Paginator(posts, 10)
        
        # Get page request and return corresponding page object.
        page_num = request.GET.get("page")
        page_obj = page.get_page(page_num)
        return render(request, "network/index.html", {'page_obj': page_obj})
    
    elif view == "following":
        # Use pagination to create page objects.
        followed_users = Follow.objects.filter(follower=request.user).values_list('followed', flat=True)
        posts = Post.objects.filter(author__in=followed_users).order_by('-timestamp')
        page = Paginator(posts, 10)
        
        # Get page request and return corresponding page object.
        page_num = request.GET.get("page")
        page_obj = page.get_page(page_num)
        return render(request, "network/index.html", {'page_obj': page_obj})
    
def load_user_profile(request, profile_username):
    user = User.objects.get(username=profile_username)
    posts = Post.objects.filter(author=user).order_by('-timestamp')
    page = Paginator(posts, 10)
    page_num = request.GET.get("page")
    page_obj = page.get_page(page_num)
    return render(request, "network/profile.html", {
        "user": user,
        "followers": Follow.objects.filter(followed=user).count(),
        "following": Follow.objects.filter(follower=user).count(),
        "page_obj": page_obj,
    })

#### FUNCTIONS ####
def create_post(request):
    if request.method == "POST":
        content = request.POST['content']
        author = User.objects.get(pk=request.user.id)
        post = Post(content=content, author=author)
        post.save()
        return HttpResponseRedirect(reverse(index))

def edit_post(request, post_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            post = get_object_or_404(Post, id=post_id)
            
            if post.author != request.user:
                return JsonResponse({'message': 'You are not authorized to edit this post.'})
            
            post.content = data.get('content', post.content)
            post.save()
            return JsonResponse({'message': 'Post updated.'})
        
        except Exception as e:
            return JsonResponse({'message': 'Error updating post: ' + str(e)})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user == post.author:
        post.delete()
        return JsonResponse({'message': 'Post deleted.'})
    else:
        return JsonResponse({'message': 'You are not authorized to delete this post.'})

def like_handler(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        post.toggle_like(request.user)
        post.liked = not post.liked
        post.save()
        return JsonResponse({'liked': post.liked, 'like_count': post.like_count})
    
def follow_handler(request, username):
    if request.user.is_authenticated:
        current_user = request.user
        followed_user = get_object_or_404(User, username=username)
        if current_user != followed_user:
            try:
                Follow.objects.get(follower = current_user, followed = followed_user).delete()
                return JsonResponse({
                    'message': 'Follow object deleted.',
                    'buttonContext': 'Follow'   
                    })
            except Follow.DoesNotExist:
                Follow(follower = current_user, followed = followed_user).save() 
                return JsonResponse({
                    'message': 'Follow object saved.',
                    'buttonContext': 'Unfollow'
                    })
                
        else:
            return JsonResponse({'message': 'You cannot follow yourself!'})
        
    
#### ACC-RELATED ROUTES ####
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")