from django.core.validators import BaseValidator
from rest_framework.exceptions import ValidationError


class CommentValidator:
    def __call__(self, attrs, serializer, *args, **kwargs):
        product = serializer.data.get("product")
        parent_comment = serializer.data.get("parent_comment")

        if product.id != parent_comment.parent_comment.id:
            raise ValidationError("Cannot add comment to this comment")

