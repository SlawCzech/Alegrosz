from products.models import Category, Product


def test_category_gui_representation():
    category = Category(name="Kartoffeln")

    assert str(category) == "Kartoffeln"


def test_add_product_to_category(product_db, category_db):
    category_db.products.add(product_db)

    potato = Category.objects.get(name="Potato")

    assert potato.products.first() == product_db


def test_get_category_name_from_product(product_db, category_db):
    category_db.products.add(product_db)

    product = Product.objects.first()

    assert product.categories.first().name == category_db.name
