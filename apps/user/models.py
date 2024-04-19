from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.cache import cache
from apps.core.models import TimeStampedModel
from apps.user.managers import UserManager
from apps.user.validators import phone_validator


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    class Gender(models.TextChoices):
        MALE = "m", _("Мужчина")
        FEMALE = "f", _("Женщина")

    _id = models.IntegerField(unique=True, db_index=True, null=True)
    first_name = models.CharField(max_length=64, verbose_name=_("First name"))
    last_name = models.CharField(max_length=64, verbose_name=_("Last name"))
    middle_name = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Middle name"))
    phone_number = models.CharField(max_length=13,
                                    unique=True, null=True, blank=True, db_index=True, validators=[phone_validator],
                                    verbose_name=_("Phone number"))
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name=_("Email"))
    bio = models.TextField(null=True, blank=True, verbose_name=_("Bio"))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_("Date of birth"))
    gender = models.CharField(max_length=12, choices=Gender.choices, verbose_name=_("Gender"), null=True, blank=True)
    username = models.CharField(
        _("username"),
        null=True,
        blank=True,
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            "unique": _("Имя пользователя уже занято."),
        },
    )

    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def save(self, *args, **kwargs):
        if not self._id and self.id is not None:
            self._id = 9999 + self.id
        if not self.username:
            self.username = None
        if not self.email:
            self.email = None
        return super().save(*args, **kwargs)

    @property
    def age(self):
        """
        Return age using `date_of_birth`
        """
        today = timezone.now().today()
        if self.date_of_birth:
            return (today.year - self.date_of_birth.year) - int(
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"


def getKey(key):
    return cache.get(key)


def setKey(key, value, timeout):
    cache.set(key, value, timeout)
