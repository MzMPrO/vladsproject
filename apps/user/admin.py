from django.contrib import admin

from apps.user.forms import UserAdminChangeForm, UserAdminCreationForm
from apps.user.models import User
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _


class UserAdmin(auth_admin.UserAdmin, ImportExportModelAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "phone_number", "gender", "date_of_birth")},
        ),
        (
            _("Other info"),
            {"fields": ("bio",)},
        ),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (_("Dates"), {"fields": ("last_login", "date_joined")}),
        (None, {"fields": ("email", "password")}),
    )
    list_display = [
        "_id",
        "phone_number",
        "first_name",
        "last_name",
        "email",
        "is_superuser",
    ]
    list_filter = auth_admin.UserAdmin.list_filter
    search_fields = ["first_name", "last_name"]
    ordering = ["id"]


admin.site.register(User, UserAdmin)
