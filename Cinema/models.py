from django.db import models
from datetime import datetime
from os.path import splitext
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from PersonalCabinet.models import UserPrivacy


STATUSES = (
    ('nl', 'Не просмотрено'),
    ('l', 'Просмотрено'),
    ('p', 'Запланировано'),
    ('t', 'Брошено'),
)


def get_timestamp_path(instance, filename):
    return '%s%s' % (datetime.now().timestamp(), splitext(filename)[1])


# Create your models here.
class Genre(models.Model):
    title = models.CharField(max_length=30)
    url = models.SlugField(null=True, blank=True, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class FilmCollection(models.Model):
    title = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Колекция фильмов'
        verbose_name_plural = 'Колекции фильмов'


class Film(models.Model):
    url = models.SlugField(null=True, blank=True, unique=True)
    title = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=get_timestamp_path)
    genres = models.ManyToManyField(Genre)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    filmCollection = models.ForeignKey(FilmCollection, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-rating']
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class UserFilmStatus(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    filmId = models.ForeignKey(Film, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUSES, default='nl')

    class Meta:
        verbose_name = 'Статус фильма пользователя'
        verbose_name_plural = 'Статусы фильмов пользователей'


class RatingStar(models.Model):
    value = models.IntegerField()

    def __str__(self):
        return str(self.value)


class RatingFilm(models.Model):
    filmId = models.ForeignKey(Film, on_delete=models.CASCADE, null=True, blank=True)
    stars = models.ForeignKey(RatingStar, on_delete=models.CASCADE, null=True, blank=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Рейтинг фильма'
        verbose_name_plural = 'Рейтинг фильмов'


class Review(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв на фильм'
        verbose_name_plural = 'Отзывы на фильмы'


def pre_save_film(sender, **kwargs):
    senderFilmId = kwargs['instance'].id
    try:
        rating = sum([rating.stars.value for rating in list(RatingFilm.objects.filter(filmId=senderFilmId))]) / len(RatingFilm.objects.filter(filmId=senderFilmId))
    except:
        rating = 0
    kwargs['instance'].rating = rating


def post_save_user(sender, **kwargs):
    sender_user = kwargs['instance']

    if not UserPrivacy.objects.filter(user=sender_user).exists():
        obj = UserPrivacy()
        obj.user = sender_user
        obj.save()


pre_save.connect(pre_save_film, sender=Film)
post_save.connect(post_save_user, sender=User)
