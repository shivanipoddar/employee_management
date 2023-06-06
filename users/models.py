from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


class UserModel(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.IntegerField()
    address = models.TextField()
    password = models.CharField(_('password'), max_length=128)
    created_on = models.DateTimeField(auto_now=True)
    document = models.FileField(upload_to='documents/')
    is_admin = models.BooleanField(default=False)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.first_name
