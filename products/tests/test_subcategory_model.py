from products.models import Subcategory


def test_subcategory_gui_representation(category_db):
    subcategory = Subcategory(name="Onions", category=category_db)

    assert str(subcategory) == "Onions"


def test_add_product_to_subcategory(product_db, category_db):
    subcategory = Subcategory.objects.create(name="Onions", category=category_db)
    subcategory.products.add(product_db)

    subcategory_db = Subcategory.objects.get(name="Onions")

    assert subcategory_db.products.first().name == product_db.name
    assert subcategory_db.category.name == category_db.name
