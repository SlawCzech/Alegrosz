from rest_framework import status
from rest_framework.test import APIRequestFactory

from products.viewsets import ProductViewSet


def test_product_viewsets(product_db, api_rf):
    url = "/api/v1/products/1/"
    view = ProductViewSet.as_view({"get": "retrieve"})

    request = api_rf.get(url)
    response = view(request, pk=product_db.pk)

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("name") == product_db.name


def test_product_viewset_with_empty_db(db, api_rf):
    url = "/api/v1/products/1/"
    view = ProductViewSet.as_view({"get": "retrieve"})

    request = api_rf.get(url)
    response = view(request, pk=1)

    assert response.status_code == status.HTTP_404_NOT_FOUND
