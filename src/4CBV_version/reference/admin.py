from django.contrib import admin

# Register your models here.
from . import models


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class SerieAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'description')


admin.site.register(models.Genre, GenreAdmin)
admin.site.register(models.Serie, SerieAdmin)
admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Publisher, PublisherAdmin)
