import faker_commerce
import pytest
from faker import Faker

from products.models import Product

fake = Faker("pl_PL")
fake.add_provider(faker_commerce.Provider)


@pytest.fixture
def product():
    """Fixture for creating Product without saving to database.
    :return: Product class object representing database row.
    :rtype: Product
    """
    name = "Polish onion"
    return Product(
        name=name,
        description=fake.sentence(),
        price=fake.ecommerce_price(),
        image=fake.file_name(category='image', extension="png"),
        stock_count=fake.unique.random_int(min=1, max=100),
        barcode=fake.ean(length=13)
    )


@pytest.fixture
def product_db(product, db):
    """Fixture for creating Product.
    :param product:
    :param db: DB fixture for database handling.
    :return: Product class object representing database row.
    :rtype: Product
    """
    product.save()
    return product


@pytest.fixture
def api_rf():
    from rest_framework.test import APIRequestFactory
    return APIRequestFactory()

