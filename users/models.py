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
    admin_type = models.CharField(max_length=50, choices=((t.name, t.value) for t in AdminType), blank=True)
    user_type = models.CharField(max_length=50, choices=((t.name, t.value) for t in UserType), blank=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extra_info')

    def __str__(self):
        return 'User (id={}, user_id={}, user_type={}, admin_type={})' \
            .format(self.id, self.user_id, self.user_type, self.admin_type)


def is_super_user(self):
    if self.extra_info is not None:
        return self.extra_info.admin_type == AdminType.SUPER_ADMIN.name
    return False


User.add_to_class('is_super_user', is_super_user)
