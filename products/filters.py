from django_filters import rest_framework as filters

from products.models import Product


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {"price": ["lt", "gt", "lte", "gte"], "name": ["exact"]}


# jak pofiltrować po nazwie kategorii
# i dlaczego contains nie działa
