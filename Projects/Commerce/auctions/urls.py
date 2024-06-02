from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/create", views.create_listing, name="create_listing"),
    path("view_listing/<int:id>", views.view_listing, name="view_listing"),
    path("watchlist_add/<int:id>", views.watchlist_add, name="watchlist_add"),
    path("watchlist_remove/<int:id>", views.watchlist_remove, name="watchlist_remove"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("your_listings", views.your_listings, name="your_listings"),
    path("won_listings", views.won_listings, name="won_listings"),
    path("place_bid/<int:id>", views.place_bid, name="place_bid"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("close_auction/<int:id>", views.close_auction, name="close_auction")
]
