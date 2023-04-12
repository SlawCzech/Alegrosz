from rest_framework import generics

from .models import Category
from .paginators import CustomPaginator
from .serializers import CategorySerializer, CategoryWithSubcategoriesSerializer


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = CustomPaginator


class CategoryRetrieveView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class SubcategoryWithSubcategoriesRetrieveView(generics.RetrieveAPIView):
    serializer_class = CategoryWithSubcategoriesSerializer
    queryset = Category.objects.all()
