from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('books/', views.books, name='books'),
    path('books/<int:pk>/', views.book_details, name='book_details'),
    path('books/add/', views.add_book, name='add_book'),

    path('books/<int:pk>/add/', views.add_edition, name='add_edition'),

    path('borrow/<int:pk>', views.borrow, name='borrow'),
    path('return/<int:pk>', views.return_book, name='return'),

    path('authors/add', views.add_author, name='add_author'),
    path('categories/add', views.add_category, name='add_category')
]