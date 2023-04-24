from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ReadOnlyField

from users.serializers import CustomUserSerializer
from . import models
from .models import Comment
from .validators import CommentValidator


class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = ('id', 'product', 'author', 'content', 'created_at', 'parent_comment')
        read_only_fields = ('product',)
        validators = [CommentValidator()]

    @staticmethod
    def validate_parent_comment(value):
        if value.parent_comment:
            raise ValidationError("Cannot add another subcomment.")
        return value
