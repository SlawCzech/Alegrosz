from rest_framework import serializers

from products.models import Product, Category, Subcategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ("id", "name")


class CategoryWithSubcategoriesSerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ("id", "name", "subcategories")


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    subcategories = SubcategorySerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "image",
            "popularity",
            "rank",
            "barcode",
            "categories",
            "subcategories",
            "stock_count",
            "description"
        )  # to jest określone w modelach!!!

    # def save(self, *args, **kwargs):
    #     self.data.categories