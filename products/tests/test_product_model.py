import faker_commerce
import pytest
from django.db import IntegrityError

from conftest import fake
from products.models import Product


def test_correct_gui_representation(product):
    name = product.name

    assert str(product) == name


def test_auto_slug(product_db):
    assert product_db.slug == "polish-onion"


def test_custom_slug(product, db):
    product.slug = "test-custom-slug"
    product.save()
    product_db = Product.objects.first()
    assert product_db.slug == 'test-custom-slug'


@pytest.mark.skip(reason="WIP")
def test_custom_invalid_slug(db):
    name = fake.ecommerce_name()
    product = Product(
        name=name,
        description=fake.sentence(),
        price=fake.ecommerce_price(),
        image=fake.file_name(category='image', extension="png"),
        stock_count=fake.unique.random_int(min=1, max=100),
        barcode=fake.ean(length=13),
        slug="test&custom-slug"
    )
    assert product.slug == 'test-custom-slug'


def test_slug_uniqueness(product_db, db):
    name = product_db.name
    with pytest.raises(IntegrityError) as excinfo:
        Product.objects.create(
            name=name,
            description=fake.sentence(),
            price=fake.ecommerce_price(),
            image=fake.file_name(category='image', extension="png"),
            stock_count=fake.unique.random_int(min=1, max=100),
            barcode=fake.ean(length=13)
        )
        assert "UNIQUE constraint failed: products_product.slug" in str(excinfo.value)
