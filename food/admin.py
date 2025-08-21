from django.contrib import admin
from .models import Restaurant, Category, MenuItem, Order, OrderItem

admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(MenuItem)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('menu_item', 'quantity', 'price')
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'restaurant', 'total_price', 'status', 'created_at')
    inlines = [OrderItemInline]

