from django.contrib import admin
from . import models

# Register your models here.


class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition """

    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    inlines = (PhotoInline,)

    list_display = (
        "name",
        "photo_number",
    )

    ordering = ("-pk",)
