from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True

class Category(TimeStampedModel):
    def __str__(self):
        return self.name
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=20)

class Budget(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    limit_amount = models.DecimalField(max_digits=10,decimal_places=2)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

# #class Alert(TimeStampedModel):
#     user_id  = models.Foreignkey(User, on_delete=models.CASCADE)
#     alert_type = models.CharField(max_length=20)
#     related_budget_id = models.ForeignKey(Budget, on_delete=models.CASECADE)
#     message = models.CharField()
#     is_read = models.BooleanField()

# Create your models here.
