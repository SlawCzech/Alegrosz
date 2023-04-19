from django.contrib.auth.decorators import permission_required
from rest_framework import status, parsers
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as filters

from . import models
from . import serializers
from .filters import ProductFilter
from .paginators import CustomPaginator
from .permissions import IsAuthor, IsStaff, HasAddProductPermission


class ProductViewSet(ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]
    pagination_class = CustomPaginator
    permission_classes = [AllowAny, IsStaff, IsAuthor, IsAuthenticated, HasAddProductPermission]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset.order_by("-id"))
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        products = self.serializer_class(queryset, many=True)

        return Response(data=products.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, pk=None, **kwargs):
        product = get_object_or_404(queryset=self.get_queryset(), pk=pk)
        return Response(data=self.serializer_class(product).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = serializers.AddProductWithCategoriesAndSubcategoriesSerializer(data=request.data,
                                                                                    context={'request': request})
        serializer.is_valid(raise_exception=True)
        product = serializer.create({**serializer.validated_data, "owner": request.user})

        product_serializer = serializers.ProductSerializer(product)

        return Response(product_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, pk=None, **kwargs):
        pass

    def partial_update(self, request, *args, pk=None, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action == "destroy":
            permission_classes = [IsAuthor]
        elif self.action == 'partial_update':
            permission_classes = [IsStaff]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, HasAddProductPermission]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
