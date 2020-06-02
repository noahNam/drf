from django.contrib.auth.models import AbstractUser
from django.db import models

"""
    AbstractBaseUser
    AbstractUser
"""


# Create your models here.
# AbstractUser 혹은 AbstractBaseUser 중에 상속받는다.
class User(AbstractUser):
    age = models.IntegerField(default=0)

    def __str__(self):
        return '이메일 : {}, 나이 {}'.format(self.email, self.age)
