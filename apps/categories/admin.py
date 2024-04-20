# from typing import Any

# from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
# from django.db.models.query import QuerySet
# from django.http.request import HttpRequest
from django.utils.safestring import mark_safe
from django_mptt_admin.admin import DjangoMpttAdmin

from apps.categories.models import Category


@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin):
    list_display = [
        "order",
        "name",
        "parent",
        "icon_tag",
    ]
    search_fields = [
        "name",
    ]

    @admin.display(description="Иконка")
    def icon_tag(self, obj):
        return mark_safe('<img src="%s" width="32" height="32" />' % (obj.icon.url if obj.icon else ""))

    # def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
    #     qs = super().get_queryset(request)
    #     return qs.filter(parent=1)
