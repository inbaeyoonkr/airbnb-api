from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


# Register your models here.
@admin.register(models.User)
class UserAdmin(UserAdmin):
    """ User Admin Definition """

    fieldsets = UserAdmin.fieldsets + (
        ("Custom Profile", {"fields": ("avatar", "is_superhost", "favs")},),
    )

    filter_horizontal = ("favs",)

    list_display = UserAdmin.list_display + ("room_count",)
