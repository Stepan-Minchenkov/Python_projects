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

    def __repr__(self):
        return self.name


class Serie(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.description:
            return f"{self.name:20}  {self.description:100}"
        else:
            return f"{self.name}"

    def __repr__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.description:
            return f"{self.name}  {self.description}"
        else:
            return f"{self.name}"

    def __repr__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.description:
            return f"{self.name:20}  {self.description:100}"
        else:
            return f"{self.name:20}  {' ':100}"

    def __repr__(self):
        return self.name
