import factory
import faker_commerce
import pytest
from faker import Faker
from pytest_factoryboy import register

from products.models import Product

fake = Faker("pl_PL")
fake.add_provider(faker_commerce.Provider)


@pytest.fixture
def product_onion():
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


@pytest.fixture
def products_batch(db):
    return ProductFactory.create_batch(60)
