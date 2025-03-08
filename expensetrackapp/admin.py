from django.contrib import admin
from .models import Category, Budget, Expense, UserProfile

from django.contrib import admin


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["user", "expense_name", "category", "amount", "date"]
    list_filter = ["user", "category"]
    search_fields = ["expense_name", "date", "category__name", "user__username"]



    


admin.site.register(Category)
admin.site.register(Budget)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(UserProfile)