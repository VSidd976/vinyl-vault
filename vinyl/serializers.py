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

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Label
        fields = ["id", "name", "country"]

class RecordReadSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    label = LabelSerializer(read_only=True)
    genres = GenreSerializer(read_only=True)

    class Meta:
        model = models.Record
        fields = [
            "id", "title", "artist", "label", "genres",
            "release_year", "price", "stock_quantity", 
            "description"
        ]

class RecordWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Record
        fields = [
            "id", "title", "artist", "label", "genres",
            "release_year", "price", "stock_quantity", 
            "description"
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ціна повинна бути більшою за 0")
        return value

    def validate_release_year(self, value):
        if value < 1900 or value > 2100:
            raise serializers.ValidationError("Вкажіть коректний рік релізу (між 1900 та 2100)")
        return value
