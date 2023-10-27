from django.urls import reverse
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Pereval, Coordinates, Tourist, Level
from .serializers import PerevalSerializer
import json
from datetime import datetime
from django.utils import timezone

class PerevalApiTestCase(APITestCase):

    def set_up(self):
        user_1 = Tourist.objects.create(
                                        email='Fortest_1',
                                        phone_number=123456789,
                                        first_name='Александр',
                                        last_name='Иванов',
                                        patronymic='Михайлович'
                                        )
        user_2 = Tourist.objects.create(
                                        email='Fortest_2',
                                        phone_number=987654321,
                                        first_name='Екатерина',
                                        last_name='Попова',
                                        patronymic='Андреевна'
                                        )
        coords_1 = Coordinates.objects.create(
                                                latitude=61.4554,
                                                longitude=59.2741,
                                                height=1200
        )
        coords_2 = Coordinates.objects.create(
                                                latitude=43.0257,
                                                longitude=43.0815,
                                                height=4308
        )
        level_1 = Level.objects.create(
                                        winter='4b',
                                        summer='2b',
                                        autumn='',
                                        spring=''
        )
        level_2 = Level.objects.create(
                                        winter='3b',
                                        summer='1b',
                                        autumn='',
                                        spring=''
        )
        self.pereval_1 = Pereval.objects.create(
                                                user=user_1,
                                                beauty_title='beauty_title_1',
                                                title="Перевал Дятлова",
                                                other_titles='other_titles_1',
                                                coordinates=coords_1,
                                                level=level_1,
                                                add_time=""
        )
        self.pereval_2 = Pereval.objects.create(
                                                user=user_2,
                                                beauty_title='beauty_title_2',
                                                title="Пик Пушкина",
                                                other_titles='other_titles_2',
                                                coordinates=coords_2,
                                                level=level_2,
                                                add_time=""
        )

    def test_get_list(self):
        url = reverse('pereval-list')
        response = self.client.get(url)
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.json())

    def test_get_detail(self):
        url = reverse('pereval-detail', args=(self.pereval_1.id,))
        response = self.client.get(url)
        serializer_data = PerevalSerializer(self.pereval_1).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.json())

class PerevalSerializerTestCase(TestCase):
    def set_up(self):
        user_1 = Tourist.objects.create(
                                        email='Fortest_1',
                                        phone_number=123456789,
                                        first_name='Александр',
                                        last_name='Иванов',
                                        patronymic='Михайлович'
        )
        user_2 = Tourist.objects.create(
                                        email='Fortest_2',
                                        phone_number=987654321,
                                        first_name='Екатерина',
                                        last_name='Попова',
                                        patronymic='Андреевна'
        )

        coords_1 = Coordinates.objects.create(
                                                latitude=61.4554,
                                                longitude=59.2741,
                                                height=1200
        )
        coords_2 = Coordinates.objects.create(
                                                latitude=43.0257,
                                                longitude=43.0815,
                                                height=4308
        )
        level_1 = Level.objects.create(
                                        winter='4b',
                                        summer='2b',
                                        autumn='',
                                        spring=''
        )
        level_2 = Level.objects.create(
                                        winter='3b',
                                        summer='1b',
                                        autumn='',
                                        spring=''
        )

        self.pereval_1 = Pereval.objects.create(
                                                user=user_1,
                                                beauty_title="beauty_title_1",
                                                title="Перевал Дятлова",
                                                other_titles="other_titles_1",
                                                coordinates=coords_1,
                                                level=level_1,
                                                add_time=""
        )
        self.pereval_2 = Pereval.objects.create(
                                                user=user_2,
                                                beauty_title="beauty_title_2",
                                                title="Пик Пушкина",
                                                other_titles="other_titles_2",
                                                coordinates=coords_2,
                                                level=level_2,
                                                add_time=""
        )

    def test_check(self):
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2], many=True).data

        expected_data = [
            {
                "id": 1,
                "user": {
                    "email": "Fortest_1",
                    "phone": "123456789",
                    "first_name": "Александр",
                    "last_name": "Иванов",
                    "patronymic": "Михайлович"
                },
                "beauty_title": "beauty_title_1",
                "title": "Перевал Дятлова",
                "other_titles": "other_titles_1",
                "add_time": str(self.pereval_1.add_time),
                "connect": None,
                "coordinates": {
                    "latitude": 61.4554,
                    "longitude": 59.2741,
                    "height": 1200
                },
                "level": None,
                "photo": []
            },
            {
                "id": 2,
                "user": {
                    "email": "Fortest_2",
                    "phone": "987654321",
                    "first_name": "Екатерина",
                    "last_name": "Попова",
                    "patronymic": "Андреевна"
                },
                "beauty_title": "beauty_title_2",
                "title": "Пик Пушкина",
                "other_titles": "other_titles_2",
                "add_time": str(self.pereval_2.add_time),
                "connect": None,
                "coordinates": {
                    "latitude": 43.0257,
                    "longitude": 43.0815,
                    "height": 4308
                },
                "level": None,
                "photo": []
            }
        ]

        self.assertEqual(serializer_data, expected_data)