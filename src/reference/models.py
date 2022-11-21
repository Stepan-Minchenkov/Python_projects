from django.db import models
from django.urls import reverse_lazy


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return f"{self.name:20}  {self.surname:20}"

    def __repr__(self):
        if self.description:
            return f"{self.name:20}  {self.surname:20}  {self.description:100}"
        else:
            return f"{self.name:20}  {self.surname:20}"

    def get_absolute_url(self):
        # return f'/ref/author/{self.pk}'
        return reverse_lazy('reference:author-detail', kwargs={'pk': self.pk})


class Serie(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.description:
            return f"{self.name:20}  {self.description:100}"
        else:
            return f"{self.name}"

    def get_absolute_url(self):
        return reverse_lazy('reference:series-detail', kwargs={'pk': self.pk})


class Genre(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.description:
            return f"{self.name:20}  {self.description:100}"
        else:
            return f"{self.name}"

    def get_absolute_url(self):
        return reverse_lazy('reference:genre-detail', kwargs={'pk': self.pk})


class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True, default='')

    def __str__(self):
        return self.name

    def __repr__(self):
        if self.description:
            return f"{self.name:20}  {self.description:100}"
        else:
            return f"{self.name:20}"

    def get_absolute_url(self):
        return reverse_lazy('reference:publish-detail', kwargs={'pk': self.pk})
