import django_filters
from rest_framework.response import Response

from .serializers import *
from rest_framework import viewsets


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
    filterset_fields = ["tourist__email"]

    def partial_update(self, request, *args, **kwargs):
        record = self.get_object()
        if record.status == 'new':
            serializer = PerevalSerializer(record, data=request.data, partial=True)
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