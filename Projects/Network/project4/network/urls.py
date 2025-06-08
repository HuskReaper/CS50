from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.create_post, name="new_post"),
    path("edit_post/<str:post_id>", views.edit_post, name="edit_post"),
    path("delete_post/<str:post_id>", views.delete_post, name="delete_post"),
    path("load_posts/<str:view>", views.load_posts, name="view"),
    path("profile/<str:profile_username>", views.load_user_profile, name="profile"),
    path("like/<str:post_id>", views.like_handler, name="like"),
    path("follow/<str:username>", views.follow_handler, name="follow")
]