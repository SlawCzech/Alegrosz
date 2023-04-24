from django.contrib.auth import get_user_model
from django.db import models


class Comment(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.DO_NOTHING, related_name="comments")
    author = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.DO_NOTHING, related_name="replies"
    )

    def __str__(self):
        return str(self.author) + ", " + (self.content if len(self.content) < 10 else self.content[:10] + "...")

