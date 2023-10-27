import django_filters
from rest_framework.response import Response
from .serializers import *
from rest_framework import viewsets, generics
from django.http import JsonResponse
from .models import Pereval

class TouristViewSet(viewsets.ModelViewSet):
    queryset = Tourist.objects.all()
    serializer_class = TouristSerializer

class CoordsViewSet(viewsets.ModelViewSet):
    queryset = Coordinates.objects.all()
    serializer_class = CoordsSerializer


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class PhotosViewSet(viewsets.ModelViewSet):
    queryset = Photos.objects.all()
    serializer_class = PhotosSerializer


class PerevalViewSet(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["user__email"]

# создание объекта перевалов
    def create(self, request, *args, **kwargs):
        serializer = PerevalSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': None,
                'id': serializer.data['id'],
            })
        if status.HTTP_400_BAD_REQUEST:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Bad Request',
                'id': None,
            })

        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Ошибка подключения к базе данных',
                'id': None,
            })

# редактирование объектов перевалов при статусе new
    def partial_update(self, request, *args, **kwargs):
        record = self.get_object()
        if record.status == 'new':
            serializer = PerevalSerializer(record, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'state': '1',
                    'message': 'Запись успешно изменена'
                })
            else:
                return Response({
                    'state': '0',
                    'message': serializer.errors
                })
        else:
            return Response({
                'state': '0',
                'message': f"Данные менять нельзя, так как они были переданы модератору "
                           f"и имеют статус: {pereval.get_status_display()}"
            })

# список данных обо всех объектах, которые пользователь с почтой <email> отправил на сервер.
class EmailAPIView(generics.ListAPIView):
    serializer_class = PerevalSerializer
    def get_email(self, request, *args, **kwargs):
        email = kwargs.get('email', None)
        if Pereval.objects.filter(user__email=email):
            data = PerevalSerializer(Pereval.objects.filter(user__email=email), many=True).data
        else:
            data = {
                'message': f'Не существует пользователя с таким email - {email}'
            }
        return JsonResponse(data, safe=False)