from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now  # Add this import

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    created_at = models.DateTimeField(default=now, editable=False)  # Set default


    def __str__(self):
        return self.name
