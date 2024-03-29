import uuid
from django.db import models

# Create your models here.
class AbstractBaseUserModel(models.Model):
    """
    Base abstract model, that has `uuid` instead of `id` and includes `created_at`, `updated_at` fields.
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True, null=True)

    UUID_FIELD = 'uuid'

    class Meta:
      abstract = True
      
      def __repr__(self):
        return f'<{self.__class__.__name__} {self.uuid}>'

class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField('Created at', auto_now_add=True, null=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True, null=True)

    class Meta:
      abstract = True
      
      def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'