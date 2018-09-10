import django_filters
from .models import Publish, Author, Book             


class PublishFilter(django_filters.rest_framework.FilterSet):
    """
    过滤类
    """
    class Meta:
        model = Publish
        fields = ['name', 'city']


class AuthorFilter(django_filters.rest_framework.FilterSet):

    class Meta:
        model = Author
        fields = ['name', 'email']


# 关联表道的搜索有待更新
class BookFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Book
        fields = ['name']
