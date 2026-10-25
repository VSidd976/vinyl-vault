from django.db import models

# Create your models here.

class Artist(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Label(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Record(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="records")
    label = models.ForeignKey(Label, on_delete=models.CASCADE, related_name="records")
    genres = models.ManyToManyField(Genre, related_name="records")
    title = models.CharField(max_length=255)
    release_year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.artist}"
