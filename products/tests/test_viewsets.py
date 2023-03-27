import pytest
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


def test_product_list_viewset(product_db, api_rf):
    url = "/api/v1/products/"
    view = ProductViewSet.as_view({"get": "list"})

    request = api_rf.get(url)
    response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("count") == 1
    assert response.data.get("next") is None
    assert response.data.get("previous") is None
    assert len(response.data.get("results")) == 1


def test_product_list_viewset_with_empty_db(db, api_rf):
    url = "/api/v1/products/"
    view = ProductViewSet.as_view({"get": "list"})

    request = api_rf.get(url)
    response = view(request)

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("count") == 0
    assert response.data.get("next") is None
    assert response.data.get("previous") is None
    assert len(response.data.get("results")) == 0


@pytest.mark.skip(reason="WIP")
def test_product_factory(product):
    products_list = [product for _ in range(60)]
    assert product.name == "Onion"
