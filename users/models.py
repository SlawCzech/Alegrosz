from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom User placeholder."""

    shoe_size = models.FloatField()

    def __str__(self) -> str:
        return str(self.shoe_size)

    def get_canonical_url(self) -> str:
        """Generate canonical url for custom user.

        :returns: canonical url
        :rtype: str
        """
        return f"/{self.shoe_size}/canonical/"
