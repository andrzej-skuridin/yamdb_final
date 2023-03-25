from django.contrib import admin
from import_export import resources, widgets
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from .models import Category, Comment, Genre, GenreTitle, Review, Title, User


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    resource_classes = (GenreResource,)
    list_display = ('name', 'slug')


class TitleResource(resources.ModelResource):
    class Meta:
        model = Title
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'category'
                  )


@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    resource_classes = (TitleResource,)
    list_display = ('name',
                    'year',
                    'rating',
                    'description',
                    'category'
                    )


class GenreTitleResource(resources.ModelResource):
    title = Field(
        attribute='title',
        column_name='title_id',
        widget=widgets.ForeignKeyWidget)
    genre = Field(
        attribute='genre',
        column_name='genre_id',
        widget=widgets.ForeignKeyWidget)

    class Meta:
        model = GenreTitle
        fields = ('id',
                  'genre_id',
                  'title_id')


@admin.register(GenreTitle)
class GenreTitleAdmin(ImportExportModelAdmin):
    resource_classes = (GenreTitleResource,)
    list_display = ('genre_id',
                    'title_id'
                    )


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = (CategoryResource,)
    list_display = ('name', 'slug')


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "role",
    )
    list_filter = ("role",)
    empty_value_display = "-пусто-"


class CommentResource(resources.ModelResource):
    review = Field(
        attribute='review',
        column_name='review_id',
        widget=widgets.ForeignKeyWidget)
    author = Field(
        attribute='author',
        column_name='author',
        widget=widgets.ForeignKeyWidget)

    class Meta:
        model = Category
        fields = ('id', 'text', 'pub_date', 'review_id', 'author')


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    resource_classes = (CommentResource,)
    list_display = ('text', 'pub_date', 'review_id', 'author')


class ReviewResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = ('id', 'text', 'pub_date', 'title_id', 'author', 'score')


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    resource_classes = (ReviewResource,)
    list_display = ('text', 'pub_date', 'title_id', 'author', 'score')


admin.site.register(User, UserAdmin)
