# user.models.py

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# accounts.models.py

class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    # user fields
    first_name  = models.CharField(blank=True, max_length=100, default="")
    last_name   = models.CharField(blank=True, max_length=100, default="")
    age         = models.IntegerField(blank=True, null=True)   
    # phone       = models.IntegerField(blank=True, null=True)   
    
    gender_choices = (
        ('Female', 'Female'), ('Male', 'Male'),
    )
    gender = models.CharField(blank=True, max_length=10, choices=gender_choices, default="")

    language_choices = (
        ('English','English'),  ('Sesotho','Sesotho'),  ('IsiXhosa','IsiXhosa'),
    )
    first_language = models.CharField(blank=True, max_length=15, choices=language_choices, default="")
    second_language = models.CharField(blank=True, max_length=15, choices=language_choices, default="")
    third_language = models.CharField(blank=True, max_length=15, choices=language_choices, default="")

    # email and email confirmation fiels
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    email_confirmed   = models.BooleanField(default=False)
    confirmed_date  = models.DateTimeField(null=True, blank=True)

    # active user; admin user; non super-user; superuser fields
    active  = models.BooleanField(default=True)
    staff   = models.BooleanField(default=False) 
    admin   = models.BooleanField(default=False) 

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name

    def get_first_name(self):
        # The user is identified by their email address
        return self.first_name

    # def info_complete(self):
    #     return self.age != None or self.gender != None or self.phone != None

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active