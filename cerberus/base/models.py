import uuid
from django.db import models
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    """
    Base model class to be imported in the all the models in the project.
    It'll append "id , created_at, modified_at, history" fields.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    modified_at = models.DateTimeField(
        auto_now=True,
    )

    history = HistoricalRecords(
        inherit=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        if kwargs.get("update_fields"):
            kwargs.update(
                {
                    "update_fields": kwargs.get("update_fields").append("modified_at"),
                }
            )

        return super().save(*args, **kwargs)
