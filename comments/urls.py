from django.urls import path
from rest_framework.routers import DefaultRouter

from . import viewsets, views

app_name = "comments"

router = DefaultRouter()
router.register(r"products/(?P<product_pk>\d+)/comments", viewsets.CommentViewSet, basename="comments-view-set")


urlpatterns = [
    *router.urls,
]
