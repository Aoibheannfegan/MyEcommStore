from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listings(models.Model):
    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Fashion & Accessories', 'Fashion & Accessories'),
        ('Home & Garden', 'Home & Garden'),
        ('Books & Media', 'Books & Media'),
        ('Health & Beauty', 'Health & Beauty'),
        ('Toys & Games', 'Toys & Games'),
        ('Arts & Crafts', 'Arts & Crafts'),
        ('Sports & Outdoor', 'Sports & Outdoor'),
        ('Vehicles & Parts', 'Vehicles & Parts'),
        ('Jewelry & Watches', 'Jewelry & Watches'),
        ('Computers & Software', 'Computers & Software'),
        ('Collectibles & Art', 'Collectibles & Art'),
        ('Musical Instruments', 'Musical Instruments'),
        ('Business & Industrial', 'Business & Industrial'),
        ('Baby & Kids', 'Baby & Kids'),
        ('Pets Supplies', 'Pets Supplies'),
        ('Travel & Experiences', 'Travel & Experiences'),
        ('Real Estate', 'Real Estate'),
        ('Tickets & Events', 'Tickets & Events'),
        ('Other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_user")
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid = models.DecimalField(max_digits=7, decimal_places=2)
    current_bid = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES, default='Electronics')
    active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="winning_user")

    def __str__(self):
        return self.title

class Bids(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bid_listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    new_bid = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.new_bid} for {self.listing.title}"
    
class Comments(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments_listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_user")
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

    def __str__(self):
        return f"{self.user.username} at {self.date}: {self.comment}"
    
class Watchlist(models.Model):
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="watchlist_listing")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")

    class Meta:
        unique_together = ("listing", "user")
