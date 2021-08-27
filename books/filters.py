import django_filters
from books.models import Book


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Title')

    class Meta:
        model = Book
        fields = ['title']
