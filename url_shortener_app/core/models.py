from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, mobile_number, email, is_active, password=None):
        """
        Creates and saves a User with the given email, mobile_number, is_active and password.
        """
        if not mobile_number:
            raise ValueError('Users must have a mobile number')
        if len(mobile_number) != 11 or mobile_number[0:2] != '09':
            raise ValueError('Invalid mobile number')

        user = self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            is_active=is_active,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Configs
    USERNAME_FIELD = 'mobile_number'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Model fields
    mobile_number = models.CharField(max_length=11, unique=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True, null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        return self.get_username()

    @classmethod
    def get_by_id(cls, user_id):
        try:
            user = cls.objects.get(pk=user_id)
            return user
        except cls.DoesNotExist:
            raise ObjectDoesNotExist

