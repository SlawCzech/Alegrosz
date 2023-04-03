import faker_commerce
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from conftest import fake
from products.models import Product


def test_correct_gui_representation(product_onion):
    name = product_onion.name

    assert str(product_onion) == name


def test_auto_slug(product_db):
    assert product_db.slug == "polish-onion"


def test_custom_slug(product_onion, db):
    product_onion.slug = "test-custom-slug"
    product_onion.save()
    product_db = Product.objects.first()
    assert product_db.slug == "test-custom-slug"


def test_custom_invalid_slug(db):
    name = fake.ecommerce_name()
    product = Product(
        name=name,
        description=fake.sentence(),
        price=fake.ecommerce_price(),
        image=fake.file_name(category="image", extension="png"),
        stock_count=fake.unique.random_int(min=1, max=100),
        barcode=fake.ean(length=13),
        slug="test&custom-slug",
    )

    with pytest.raises(ValidationError) as excinfo:
        product.save()
    assert "Enter a valid “slug” consisting of letters, numbers, underscores or hyphens." in excinfo.value.messages


def test_slug_uniqueness(product_db, db):
    name = product_db.name
    with pytest.raises(ValidationError) as excinfo:
        Product.objects.create(
            name=name,
            description=fake.sentence(),
            price=fake.ecommerce_price(),
            image=fake.file_name(category="image", extension="png"),
            stock_count=fake.unique.random_int(min=1, max=100),
            barcode=fake.ean(length=13),
        )
    assert "Product with this Slug already exists." in excinfo.value.messages
