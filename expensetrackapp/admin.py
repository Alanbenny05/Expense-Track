from django.contrib import admin
from .models import Category,Budget,Expense,UserProfile
from .models import Expense
admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(Expense)
admin.site.register(UserProfile)

# Register your models here.
