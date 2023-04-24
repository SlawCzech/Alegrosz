from products.serializers import ProductSerializer


def test_serializer_all_fields(product_db):
    serializer = ProductSerializer(instance=product_db)
    assert tuple(serializer.data.keys()) == (
        "id",
        "name",
        "description",
        "price",
        "image",
        "popularity",
        "rank",
        "barcode",
        "categories",
        "subcategories",
        "stock_count",
        "owner",
    )
