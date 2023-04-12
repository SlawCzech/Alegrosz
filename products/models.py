from django.contrib.auth import get_user_model
from django.core.validators import validate_slug
from django.db import models
from django.utils.text import slugify


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(TimeStampModel):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products")
    stock_count = models.PositiveIntegerField()
    slug = models.SlugField(blank=True, max_length=50, unique=True)
    popularity = models.PositiveIntegerField(default=0, help_text="Incremented when user views details page.")
    rank = models.FloatField(default=0, help_text="Ranked by users.")
    sales_count = models.PositiveIntegerField(default=0)
    barcode = models.CharField(max_length=13, unique=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.full_clean()
        super().save(*args, **kwargs)


class CategoryProduct(models.Model):
    product_id = models.ForeignKey("Product", on_delete=models.CASCADE)
    category_id = models.ForeignKey("Category", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    products = models.ManyToManyField("Product", related_name="categories", through="CategoryProduct")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Subcategory(models.Model):
    name = models.CharField(max_length=40)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="subcategories")
    products = models.ManyToManyField("Product", related_name="subcategories")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Subcategories"
