from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models import Sum


# 🎮 Track each game session played by a user
class GameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_name = models.CharField(max_length=100)
    score = models.PositiveIntegerField()  # Only allow non-negative scores
    played_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.game_name} - {self.score}"

    class Meta:
        ordering = ['-played_at']  # Newest scores first

    @staticmethod
    def total_score_for_user(user):
        """Method to calculate the total score for a given user."""
        return GameScore.objects.filter(user=user).aggregate(Sum('score'))['score__sum'] or 0


# 🎲 Optional: List of available games (future-friendly for admin)
class Game(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    max_score = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.name


# 🛍️ Product listing (e.g., shop or marketplace)
class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    created_at = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.name
