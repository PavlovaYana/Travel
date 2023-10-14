from django.contrib.auth.models import User
from django.db import models

#Модель Tourist содержит объекты всех туристов
#Имеет поля: ФИО, эл.почта, номер телефона и имеет связь один-к-одному с моделью User
class Tourist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=20, verbose_name='Отчество')
    email = models.EmailField(blank=False, verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=15)


    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic} {self.email} {self.phone_number}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


#Модель Coordinates содержит информацию о широте, долготе, высоте Перевалов
class Coordinates(models.Model):
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота')

    def __str__(self):
        return f'Широта:{self.latitude}, Долгота:{self.longitude}, Высота:{self.height}'

    class Meta:
        db_table = 'pereval_coords'
        verbose_name = 'Координаты'
        verbose_name_plural = 'Координаты'


LEVEL = [
    ('1a', '1A'),
    ('1b', '1Б'),
    ('2a', '2А'),
    ('2b', '2Б'),
    ('3a', '3А'),
    ('3b', '3Б'),
    ('4a', '4А'),
    ('4b', '4Б'),
    ('5a', '5А'),
    ('5b', '5Б'),
]

#Класс Level хранит в себе сложности перевалов в разные времена года
class Level(models.Model):
    winter = models.CharField(max_length=3, choices=LEVEL, verbose_name='Зима', default='')
    spring = models.CharField(max_length=3, choices=LEVEL, verbose_name='Весна', default='')
    summer = models.CharField(max_length=3, choices=LEVEL, verbose_name='Лето', default='')
    autumn = models.CharField(max_length=3, choices=LEVEL, verbose_name='Осень', default='')

    def __str__(self):
        return f'зима: {self.winter}, весна: {self.spring}, лето: {self.summer}, осень: {self.autumn}'

    class Meta:
        verbose_name = 'уровень сложности'
        verbose_name_plural = 'Уровни сложности'

#Модель Pereval содержит в себе всю информацию о перевалах, добавленных туристами
class Pereval(models.Model):
    status_choices = [
        ('new', 'Новая запись'),
        ('pending', 'Ожидает подтверждения'),
        ('accepted', 'Подтверждено'),
        ('rejected', 'Отказано')]

    beauty_title = models.CharField(max_length=10, blank=True, verbose_name='Вид объекта')
    title = models.CharField(max_length=50, verbose_name='Наименование')
    other_titles = models.CharField(max_length=255, blank=True, verbose_name='Другие наименования')
    connect = models.TextField(blank=True, verbose_name='Соединение')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    user = models.ForeignKey(Tourist, on_delete=models.CASCADE, verbose_name='Пользователь')
    coordinates = models.ForeignKey(Coordinates, on_delete=models.CASCADE, verbose_name='Координаты')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name='уровень сложности')
    status = models.CharField(max_length=20, choices=status_choices, default='new', verbose_name='Проверка статуса записи')

    def __str__(self):
        return f'{self.beauty_title} {self.title} {self.other_titles} {self.connect} {self.add_time} {self.status}' \
               f'{self.level} {self.coordinates} {self.user} {self.images}'

    class Meta:
        db_table = 'pereval'
        verbose_name = 'Перевал'
        verbose_name_plural = 'Перевалы'

#Модель Photos хранит фото перевалов
class Photos(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='photo')
    data = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото')
    title = models.CharField(max_length=255, blank=True, verbose_name='Название')

    def __str__(self):
        return f'{str(self.id)} {self.title}'

    class Meta:
        db_table = 'pereval_photos'
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'

