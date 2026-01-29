from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class BaseModel(models.Model):
    """
    Abstract base model for:
    -audit
    -ownership
    -soft delete
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    created_by  = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        on_delete=models.SET_NULL,
    )

    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
        on_delete=models.SET_NULL,
    )

    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        

