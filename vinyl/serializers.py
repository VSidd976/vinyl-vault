from rest_framework import serializers
from vinyl import models

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ["id", "name"]

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artist
        fields = ["id", "name", "country", "bio"]

class LabeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Label
        fields = ["id", "name", "country"]

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Record
        fields = [
            "id", "title", "artist", "label", "genres",
            "release_year", "price", "stock_quantity", 
            "description"
        ]
