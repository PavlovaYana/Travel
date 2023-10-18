from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from .models import Tourist, Pereval, Photos, Coordinates, Level


class TouristSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tourist
        fields = '__all__'


class PhotosSerializer(serializers.ModelSerializer):
    data = serializers.URLField()

    class Meta:
        model = Photos
        fields = ['data', 'title']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinates
        fields = '__all__'

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'

class PerevalSerializer(WritableNestedModelSerializer):
    user = TouristSerializer()
    photos = PhotosSerializer()
    coordinates = CoordsSerializer()
    level = LevelSerializer(allow_null=True)

    class Meta:
        model = Pereval
        fields = ['id', 'beauty_title', 'title', 'other_titles', 'connect', 'add_time', 'status', 'level',
                  'coordinates',
                  'user',
                  'photos']

    def create(self, validated_data):
        user = validated_data.pop('user')
        coordinates = validated_data.pop('coordinates')
        photos = validated_data.pop('photos')

        pereval_user = Tourist.objects.filter(email=user['email'])
        if pereval_user.exists():
            user_serializer = TouristSerializer(data=user)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()

        else:
            user = Tourist.objects.create(**user)

        coordinates = Coordinates.objects.create(**coordinates)
        pereval = Pereval.objects.create(**validated_data, user=user, coordinates=coordinates)

        for photo in photos:
            data = photo.pop('data')
            title = photo.pop('title')
            print(title)
            Photos.objects.create(data=data, pereval=pereval, title=title)

        return pereval