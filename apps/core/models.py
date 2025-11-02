from django.db import models

# Create your models here.
from apps.core.utils import uuid_factory


class BlankModel(models.Model):

    class Meta:
        abstract = True


class BaseModel(BlankModel):
    id = models.CharField(max_length=255, default=uuid_factory, editable=False, primary_key=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f'Row {self.guid}'


class ApiKey(BaseModel):
    host = models.URLField(null=True, blank=True)
    service_name = models.CharField(max_length=100)
    secret = models.CharField(max_length=32, default=uuid_factory, db_index=True)