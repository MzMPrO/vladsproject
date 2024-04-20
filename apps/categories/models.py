from django.core.validators import FileExtensionValidator
from django.db import models
from django.template import defaultfilters
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from unidecode import unidecode

from apps.categories.managers import CategoryManager
from apps.core.models import TimeStampedModel


class Category(TimeStampedModel, MPTTModel):
    """
    Category model
    """

    name = models.CharField(max_length=255, db_index=True, verbose_name=_("Categoty"))
    icon = models.FileField(
        upload_to="category",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["svg", "png"])],
        verbose_name=_("Иконка"),
    )
    parent = TreeForeignKey(
        "self",
        related_name="children",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Родительская категория"),
    )

    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    objects = CategoryManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_level(self):
        level = 0
        current_category = self
        while current_category.parent is not None:
            level += 1
            current_category = current_category.parent
        return level

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
