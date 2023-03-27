from django.contrib import admin

from .models import Product


class ProductAdminConfig(admin.ModelAdmin):
    """Class **ProductAdminConfig** displays products list
    in admin panel based on :class`product_onion.models.Product` model."""

    list_display = ("name", "price", "stock_count", "popularity", "rank", "sales_count")
    search_fields = ("name",)
    list_editable = ("price", "popularity", "rank", "stock_count")
    list_display_links = ("name",)
    save_on_top = True
    list_filter = ("created_at",)
    list_per_page = 50


admin.site.register(Product, ProductAdminConfig)
