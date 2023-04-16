from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Category
from .paginators import CustomPaginator
from .serializers import CategorySerializer, CategoryWithSubcategoriesSerializer


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = CustomPaginator
    permission_classes = (IsAuthenticated,)


class CategoryRetrieveView(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)


class CategoryWithSubcategoriesRetrieveView(generics.RetrieveAPIView):
    serializer_class = CategoryWithSubcategoriesSerializer
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)
