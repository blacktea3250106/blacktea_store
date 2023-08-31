from django.contrib import admin

from .models import Product, Color, Capacity, Comment, Cart

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "formatted_price", "time", "slug", "display_style_colors", "display_style_capacities")
    list_filter = ("name", "price", "time")

    def display_style_colors(self, obj):
        style_colors = ", ".join([color.name for color in obj.style_color.all()])
        return style_colors

    def display_style_capacities(self, obj):
        style_capacities = ", ".join([capacity.name for capacity in obj.style_capacity.all()])
        return style_capacities
    
    display_style_colors.short_description = "Style Colors" 
    display_style_capacities.short_description = "Style Capacities" 

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "star_num", "text", "date")

class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "display_style_colors", "display_style_capacities", "volume", "formatted_price")

    def display_style_colors(self, obj):
        style_colors = ", ".join([color.name for color in obj.style_color.all()])
        return style_colors

    def display_style_capacities(self, obj):
        style_capacities = ", ".join([capacity.name for capacity in obj.style_capacity.all()])
        return style_capacities

    display_style_colors.short_description = "Style Colors" 
    display_style_capacities.short_description = "Style Capacities" 

admin.site.register(Product, ProductAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Color)
admin.site.register(Capacity)

