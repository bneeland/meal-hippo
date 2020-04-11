from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone, address, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            address=address,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, address, password=None):
        user = self.create_user(
            email,
            password=password,
            phone=phone,
            address=address,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'address',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
