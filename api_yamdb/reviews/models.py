from django.db import models

from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxLengthValidator,
                                    validate_slug,
                                    MaxValueValidator,
                                    MinValueValidator
                                    )


class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'user'),
        ('admin', 'admin'),
        ('moderator', 'moderator'),
    ]

    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(
        'Информация о пользователе',
        help_text='Введите краткую информацию о себе',
        blank=True,
        null=True,
    )
    role = models.CharField(max_length=9, choices=ROLE_CHOICES, default='user')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Категория',
                            unique=True,
                            validators=[MaxLengthValidator(limit_value=256)]
                            )
    slug = models.SlugField(unique=True,
                            max_length=50,
                            validators=[validate_slug,
                                        MaxLengthValidator(limit_value=50)
                                        ]
                            )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['-id']

    def __str__(self):
        return f'{self.name}'


class Genre(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Жанр',
                            unique=True,
                            validators=[MaxLengthValidator(limit_value=256)]
                            )
    slug = models.SlugField(unique=True,
                            max_length=50,
                            validators=[validate_slug,
                                        MaxLengthValidator(limit_value=50)
                                        ]
                            )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.name}'


class Title(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название',
                            unique=True,
                            validators=[MaxLengthValidator(limit_value=256)]
                            )
    year = models.IntegerField(blank=True,
                               null=True,
                               verbose_name='Год выпуска')
    rating = models.FloatField(blank=True,
                               null=True)
    description = models.CharField(max_length=200,
                                   verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.name}'


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre,
                              db_column='genre_id',
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True,
                              )
    title = models.ForeignKey(Title,
                              db_column='title_id',
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True,
                              )

    class Meta:
        verbose_name = 'Жанр/Произведение'
        verbose_name_plural = 'Жанры/Произведения'
        ordering = ('-id',)


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    score = models.SmallIntegerField(
        validators=[MaxValueValidator(10),
                    MinValueValidator(1)])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-id',)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-id',)
