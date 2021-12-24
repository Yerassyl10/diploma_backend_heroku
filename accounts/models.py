from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from rest_framework.authtoken.models import Token


class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Incorrect email address!!!')
        account = self.model(email=self.normalize_email(email),)
        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_superuser(self, email, password):
        super_account = self.create_user(email=self.normalize_email(email), password=password, )
        super_account.is_staff = True
        super_account.is_superuser = True
        super_account.is_admin = True
        super_account.is_active=True
        super_account.save(using=self._db)

def profile_image_folder(instance, fname):
    return '/'.join(['profile_images', str(instance.email), fname])
def profile_cv_folder(instance, fname):
    return '/'.join(['profile_cvs', str(instance.email), fname])

class Users(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True, null=True, default=None)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    birthday = models.CharField(max_length=30, blank=True, null=True, default=None)
    prof_image = models.ImageField(null=True, upload_to=profile_image_folder)
    prof_cv = models.FileField(null=True, upload_to=profile_cv_folder)
    contact_number = models.CharField(max_length=30, blank=True, null=True)
    zipcode = models.CharField(max_length=30, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    class Meta:
        db_table = "tbl_users"

    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None): return self.is_superuser

    def has_module_perms(self, app_label): return self.is_superuser

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birthday': self.birthday,
            'prof_image': self.prof_image,
            'prof_cv': self.prof_cv,
            'contact_number': self.contact_number,
            'zipcode': self.zipcode
        }

