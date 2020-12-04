from django.contrib import admin

from .models import Category, Product, ProductImage


class ImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image', )


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
