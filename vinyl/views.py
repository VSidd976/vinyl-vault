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
        if not serializer.is_valid():
            return error_response(
                message="Помилка валідації даних артиста",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        if not serializer.is_valid():    
            return error_response(
                message="Помилка оновлення артиста",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        if not serializer.is_valid():
            return error_response(
                message="Помилка валідації лейблу",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LabelDetail(mixins.GetObjectMixin[models.Label], APIView):
    def get(self, request, pk):
        label = self.get_object(pk)
        if not label:
            return error_response("Лейбл не знайдено", status_code=status.HTTP_404_NOT_FOUND)
        serializer = serializers.LabelSerializer(label)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        label = self.get_object(pk)
        if not label:
            return error_response("Лейбл не занйдено", status_code=status.HTTP_404_NOT_FOUND)

        serializer = serializers.LabelSerializer(label, data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Помилка оновлення лейблу",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

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

class RecordList(APIView):
    def get(self, request):
        queryset = models.Record.objects.select_related("artist", "label").prefetch_related("genres").all()

        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(artist__name__icontains=search)

        genre_id = request.query_params.get("genre_id")
        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)

        label_id = request.query_params.get("label_id")
        if label_id:
            queryset = queryset.filter(label_id=label_id)

        sort_by = request.query_params.get("sort_by")
        if sort_by == "price_asc":
            queryset = queryset.order_by("price")

        elif sort_by == "price_desc":
            queryset = queryset.order_by("-price")

        elif sort_by == "yaer_asc":
            queryset = queryset.order_by("release_year")

        elif sort_by == "year_desc":
            queryset = queryset.order_by("-release_year")

        serializer = serializers.RecordReadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = serializers.RecordWriteSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Помилка валідації даних платівки",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        record = serializer.save()
        read_serializer = serializers.RecordReadSerializer(record)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

class RecordDetail(mixins.GetObjectMixin[models.Record], APIView):
    def get(self, request, pk):
        record = self.get_object(pk)
        if not record:
            return error_response("Платівку не знайдено", status_code=status.HTTP_404_NOT_FOUND)

        serializer = serializers.RecordReadSerializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        record = self.get_object(pk)
        if not record:
            return error_response("Платівку не знайдено", status_code=status.HTTP_404_NOT_FOUND)

        serializer = serializers.RecordWriteSerializer(record, data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Помилка оновлення платівки",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        update_record = serializer.save()
        read_serializer = serializers.RecordReadSerializer(update_record)
        return Response(read_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        record = self.get_object(pk)
        if not record:
            return error_response("Платівку не знайдено", status_code=status.HTTP_404_NOT_FOUND)

        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    