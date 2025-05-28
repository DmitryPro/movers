from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company_profile")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('offers', 'Waiting for offers'),
        ('offer_selected', 'Offer Selected'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    from_address = models.CharField(max_length=255)
    to_address = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    move_type = models.CharField(max_length=20, choices=[('local', 'Local'), ('interstate', 'Interstate')])
    floors_from = models.PositiveIntegerField()
    floors_to = models.PositiveIntegerField()
    items_description = models.TextField(blank=True)
    distance_km = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    chosen_offer = models.ForeignKey('Offer', null=True, blank=True, on_delete=models.SET_NULL, related_name='selected_for_order')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"

class Offer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="offers")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="offers")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Offer by {self.company.name} on Order #{self.order.id}"
