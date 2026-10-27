from django.db.models import ProtectedError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from vinyl import models
from vinyl import serializers
from vinyl.exceptions import error_response
from vinyl import mixins

# Create your views here.

class ArtistList(APIView):
    def get(self, request):
        artists = models.Artist.objects.all()
        serializer = serializers.ArtistSerializer(artists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return error_response(
            message="Помилка валідації даних артиста",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class ArtistDetail(mixins.GetObjectMixin[models.Artist], APIView):
    # def get_object(self, pk):
    #     try:
    #         return models.Artist.objects.get(pk=pk)
    #     except models.Artist.DoesNotExist:
    #         return None

    def get(self, request, pk):
        artist = self.get_object(pk)
        if not artist:
            return error_response("Артиств не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        artist = self.get_object(pk)
        if not artist:
            return error_response("Артиств не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ArtistSerializer(artist, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return error_response(
            message="Помилка оновлення артиста",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        artist = self.get_object(pk)
        if not artist:
            return error_response("Артиста не знайдено", status_code=status.HTTP_404_NOT_FOUND)

        try:
            records_count = artist.records.count()
            if records_count > 0:
                return error_response(
                    message=f"Неможливо видалити артиста {artist}, оскільки за ним закріплено {records_count} платівок",
                    status_code=status.HTTP_409_CONFLICT
                )

            artist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ProtectedError:
            return error_response(
                message="Видалення заблоковано: існують пов'язані релізи",
                status_code=status.HTTP_409_CONFLICT
            )

class ArtistRecords(mixins.GetObjectMixin[models.Artist], APIView):
    def get(self, request, pk):
        artist = self.get_object(pk)
        if not artist:
            return error_response("Артиста не знайдено", status_code=status.HTTP_404_NOT_FOUND)

        records = artist.records.all()
        serializer = serializers.RecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LabelList(APIView):
    def get(self, request):
        labels = models.Label.objects.all()
        serializer = serializers.LabeSerializer(labels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.LabeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return error_response(
            message="Помилка валідації лейблу",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

class LabelDetail(mixins.GetObjectMixin[models.Label], APIView):
    def get(self, request, pk):
        label = self.get_object(pk)
        if not label:
            return error_response("Лейбл не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = serializers.LabeSerializer(label)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        label = self.get_object(pk)
        if not label:
            return error_response("Лейбл не занйдено", status_code=status.HTTP_404_NOT_FOUND)

        serializer = serializers.LabeSerializer(label, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return error_response(
            message="Помилка оновлення лейблу",
            details=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        label = self.get_object(pk)
        if not label:
            return error_response("Лейбл не знайдено", status_code=status.HTTP_404_NOT_FOUND)

        records_count = label.records.count()
        if records_count > 0:
            return error_response(
                message=f"Неможливо видалити лейбл {label}, осклільки за ним закріплено {records_count} релізів",
                status_code=status.HTTP_409_CONFLICT
            )

        label.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    