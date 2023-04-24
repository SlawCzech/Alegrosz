from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from comments import models, serializers
from products.models import Product
from products.paginators import CustomPaginator


class CommentViewSet(ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    pagination_class = CustomPaginator

    def list(self, request, *args, **kwargs):
        pk = kwargs.get('product_pk')
        comments = self.get_queryset()
        if pk is not None:
            comments = comments.filter(product__pk=pk)

        page = self.paginate_queryset(comments.order_by("id"))
        if page is not None:
            serializer = self.serializer_class(self.get_queryset(), many=True)
            return self.get_paginated_response(serializer.data)

        comments = self.serializer_class(comments, many=True)

        return Response(data=comments.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = get_object_or_404(queryset=Product.objects.all(), pk=kwargs.get('product_pk'))
        serializer.save(author=request.user, product=product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


