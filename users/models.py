from enum import Enum

from django.contrib.auth.models import User
from django.db import models


class AdminType(Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    PROVIDER = "PROVIDER"


class UserType(Enum):
    STUDENT = "STUDENT"
    PERSONNEL = "PERSONNEL"
    GUEST = "GUEST"


class UserExtraInfo(models.Model):
    # admin_type = models.CharField(max_length=50, choices=AdminType)
    # user_type = models.CharField(max_length=50, choices=UserType)
    # remove these if not needed. I changed them because i got some errors in migration.
    admin_type = models.CharField(max_length=50, choices=((t, t.value) for t in AdminType))
    user_type = models.CharField(max_length=50, choices=((t, t.value) for t in UserType))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extra_info')
