import io
from PIL import Image
import pytest

from conftest import fake
from ..views import CategoryListView, CategoryRetrieveView, CategoryWithSubcategoriesRetrieveView
from ..models import Category, Subcategory
from ..viewsets import ProductViewSet
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile


def test_category_list_view_not_authenticated(api_rf):
    url = "/api/v1/categories/"
    view = CategoryListView.as_view()

    request = api_rf.get(url)
    response = view(request)

    assert response.status_code == 401


def test_category_list_view_with_authentication(auth_token, api_rf):
    url = "/api/v1/categories/"
    view = CategoryListView.as_view()

    Category.objects.create(name='Category 1')
    Category.objects.create(name='Category 2')

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_token)
    response = client.get(url)

    assert response.status_code == 200
    assert response.data['count'] == 2


def test_category_retrieve_view_no_authentication(api_rf):
    url = "/api/v1/categories/1/"
    view = CategoryRetrieveView.as_view()

    request = api_rf.get(url)
    response = view(request)

    assert response.status_code == 401


def test_category_retrieve_view_authenticated(auth_token, api_rf):
    url = "/api/v1/categories/1/"
    view = CategoryRetrieveView.as_view()

    Category.objects.create(name='Category 1')

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_token)
    response = client.get(url)

    assert response.status_code == 200
    assert response.data['name'] == 'Category 1'


def test_category_with_subcategories_view_no_authentication(api_rf):
    url = "/api/v1/categories/1/subcategories/"
    view = CategoryWithSubcategoriesRetrieveView.as_view()

    request = api_rf.get(url)
    response = view(request)

    assert response.status_code == 401


def test_category_with_subcategories_retrieve_view_authenticated(auth_token, api_rf):
    url = "/api/v1/categories/1/subcategories/"
    view = CategoryWithSubcategoriesRetrieveView.as_view()

    test_category = Category.objects.create(name='Category 1')
    Subcategory.objects.create(name='test_sub', category=test_category)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_token)
    response = client.get(url)

    assert response.status_code == 200


def test_create_product_with_authentication(user_with_token_and_add_permission, api_rf):
    url = "/api/v1/products/"

    image = Image.new('RGB', (100, 100), color='red')
    image_file = io.BytesIO()
    image.save(image_file, 'jpeg')
    image_file.seek(0)

    data = {
        'name': 'towar',
        'description': 'no desc',
        'price': 14,
        'image': SimpleUploadedFile('test_image.jpg', image_file.read(), content_type='image/jpeg'),
        'stock_count': fake.unique.random_int(min=1, max=100),
        'barcode': fake.ean(length=13)
    }

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_with_token_and_add_permission)

    response = client.post(url, data=data, format='multipart')

    assert response.status_code == 201
    assert response.data['name'] == 'towar'
    assert response.data['owner'] == 'testuser2'


def test_create_product_without_authentication():
    url = "/api/v1/products/"
    view = ProductViewSet.as_view({"post": "create"})

    client = APIClient()

    response = client.post(url)

    assert response.status_code == 401


def test_create_product_with_authentication_and_without_add_permission(auth_token):
    url = "/api/v1/products/"

    image = Image.new('RGB', (100, 100), color='red')
    image_file = io.BytesIO()
    image.save(image_file, 'jpeg')
    image_file.seek(0)

    data = {
        'name': 'towar',
        'description': 'no desc',
        'price': 14,
        'image': SimpleUploadedFile('test_image.jpg', image_file.read(), content_type='image/jpeg'),
        'stock_count': fake.unique.random_int(min=1, max=100),
        'barcode': fake.ean(length=13)
    }

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + auth_token)

    response = client.post(url, data=data, format='multipart')

    assert response.status_code == 403


def test_partial_update_with_staff_user(staff_user, product_db):
    url = f"/api/v1/products/{product_db.id}/"

    new_data = {"name": "new_name"}

    client = APIClient()
    client.force_authenticate(staff_user)

    response = client.patch(url, new_data)

    assert response.status_code == 200
    assert response.data["name"] == "new_name"


def test_partial_update_with_not_staff_user(user_db, product_db):
    url = f"/api/v1/products/{product_db.id}/"

    new_data = {"name": "new_name"}

    client = APIClient()
    client.force_authenticate(user_db)

    response = client.patch(url, new_data)

    assert response.status_code == 403


def test_destroy_by_product_owner(user_db, product_db):
    url = f"/api/v1/products/{product_db.id}/"

    client = APIClient()
    client.force_authenticate(user_db)

    response = client.delete(url)

    assert response.status_code == 204


def test_destroy_not_by_product_owner(staff_user, product_db):
    url = f"/api/v1/products/{product_db.id}/"

    client = APIClient()
    client.force_authenticate(staff_user)

    response = client.delete(url)

    assert response.status_code == 403
