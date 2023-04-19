from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class CustomPaginator(LimitOffsetPagination):
    page_size = 20
    page_query_param = "page"
    max_page_size = 100
