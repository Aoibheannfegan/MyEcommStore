from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:listing_id>", views.listing_page, name="listing_page"),
    path("remove/<int:listing_id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("add/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("close/<int:listing_id>", views.close_auction, name="close_auction"),
    path("comments/<int:listing_id>", views.comments, name="comments"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category")
]
