from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.description:
            return f"{self.name:20}  {self.surname:20}  {self.description:100}"
        else:
            return f"{self.name:20}  {self.surname:20}  {' ':100}"


class Serie(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.description:
            return f"{self.name:20}  {self.description:100}"
        else:
            return f"{self.name:20}  {' ':100}"


class Genre(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.description:
            return f"{self.name:20}  {self.description:100}"
        else:
            return f"{self.name:20}  {' ':100}"


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.description:
            return f"{self.name:20}  {self.description:100}"
        else:
            return f"{self.name:20}  {' ':100}"
