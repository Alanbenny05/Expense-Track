from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created_at` and `updated_at` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Updated on every save

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    """
    Represents a category for expenses.
    """
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=200)  # Increased max_length for description

    def __str__(self):
        return self.name


class Budget(TimeStampedModel):
    """
    Represents a budget limit for a specific category.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Renamed to `category`
    limit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'category'], name='unique_budget_user_category')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.limit_amount}"


class Expense(TimeStampedModel):
    """
    Represents an expense made by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_name = models.CharField(max_length=20, null=True, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)  # Added category field
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.category.name if self.category else 'No Category'}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username