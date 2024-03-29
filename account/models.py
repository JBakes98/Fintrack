import uuid
import pytz
import decimal

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from account.managers import UserAccountManager
from country.models import Country


class User(AbstractBaseUser, PermissionsMixin):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(blank=False, null=False, max_length=100)
    last_name = models.CharField(blank=False, null=False, max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    verified = models.DateTimeField(default=None, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    last_login = models.DateTimeField(default=timezone.now)
    timezone = models.CharField(max_length=50, default='UTC', choices=TIMEZONES, null=False, blank=False)

    funds = models.DecimalField(default=decimal.Decimal(0.00), max_digits=15, decimal_places=4, null=False, blank=False)
    value = models.DecimalField(default=decimal.Decimal(0.00), max_digits=15, decimal_places=4, null=False, blank=False)
    result = models.DecimalField(default=decimal.Decimal(0.00), max_digits=15, decimal_places=4, null=False, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserAccountManager()

    def __unicode__(self):
        return self.email

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)