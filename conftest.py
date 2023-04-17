import factory
import faker_commerce
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from faker import Faker
from pytest_factoryboy import register
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APIClient

from products.models import Product, Category

fake = Faker("pl_PL")
fake.add_provider(faker_commerce.Provider)


@pytest.fixture
def user_db(db, django_user_model):
    return django_user_model.objects.create_user(
        username='testUser',
        password='password1234',
        email='test@test.pl',
    )


@pytest.fixture
def product_onion(user_db):
    """Fixture for creating Product without saving to database.
    :return: Product class object representing database row.
    :rtype: Product
    """
    name = "Polish onion"
    return Product(
        name=name,
        description=fake.sentence(),
        price=fake.ecommerce_price(),
        image=fake.file_name(category="image", extension="png"),
        stock_count=fake.unique.random_int(min=1, max=100),
        barcode=fake.ean(length=13),
        owner=user_db
    )


@pytest.fixture
def product_db(product_onion, db):
    """Fixture for creating Product.
    :param product_onion:
    :param db: DB fixture for database handling.
    :return: Product class object representing database row.
    :rtype: Product
    """
    product_onion.save()
    return product_onion


@pytest.fixture
def api_rf():
    from rest_framework.test import APIRequestFactory

    return APIRequestFactory()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f"{factory.Faker('sentence', nb_words=3)} {n}")
    password = factory.Faker('word')
    email = factory.Faker('email')


@register
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'products.Product'

    name = factory.Sequence(lambda n: f"{factory.Faker('sentence', nb_words=3)} {n}")
    description = factory.Faker('paragraph')
    price = factory.Faker('pydecimal', left_digits=2, right_digits=2, positive=True, min_value=10, max_value=34)
    image = factory.Faker("image_url")
    stock_count = factory.Faker("pyint", min_value=1, max_value=50)
    barcode = factory.Faker('ean13')
    owner = factory.SubFactory(UserFactory)


@pytest.fixture
def products_batch(db):
    return ProductFactory.create_batch(60)


@pytest.fixture
def one_product():
    return ProductFactory.create_batch(1)


@pytest.fixture
def category_db(db):
    return Category.objects.create(name="Potato")


@pytest.fixture
def auth_token(db, django_user_model):
    user = django_user_model.objects.create_user(username='testuser', password='testpass')
    client = APIClient()
    response = client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpass'},
                           format='json')
    token = response.data['access']
    return token


@pytest.fixture
def user_with_token_and_add_permission(db, django_user_model):
    user = django_user_model.objects.create_user(username='testuser2', password='testpass')
    user.user_permissions.add(Permission.objects.get(codename='add_product'))
    client = APIClient()
    response = client.post(reverse('token_obtain_pair'), {'username': 'testuser2', 'password': 'testpass'},
                           format='json')
    token = response.data['access']
    return token


@pytest.fixture
def staff_user(db, django_user_model):
    return django_user_model.objects.create_user(username='staffuser', password='testpass', is_staff=True)

