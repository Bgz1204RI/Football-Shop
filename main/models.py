from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    SIZE_CHOICES = [
        ("S", "Small"),
        ("M", "Medium"),
        ("L", "Large"),
        ("XL", "Extra Large"),
    ]

    name = models.CharField(max_length=200)
    price = models.IntegerField()                         # per assignment
    description = models.TextField(blank=True)
    thumbnail = models.URLField(blank=True)
    category = models.CharField(max_length=50)

    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default="M")
    stock = models.IntegerField(default=0)

    is_featured = models.BooleanField(default=False)
    for_sale = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def stock_status(self):
        if self.stock == 0:
            return "Sold Out"
        elif self.stock < 5:
            return "Short Supply"
        return "In Stock"

    def discount_status(self):
        if self.for_sale:
            return int(self.price * 0.92)
        elif self.for_sale and self.is_featured:
            return int(self.price * 0.87)
        return self.price
    
    

