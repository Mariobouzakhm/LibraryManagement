from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('books/', views.books, name='books'),
    path('books/<int:pk>/', views.book_details, name='book_details'),
    path('books/add/', views.add_book, name='add_book'),

    path('books/<int:pk>/add/', views.add_edition, name='add_edition'),
    path('edition/<int:pk>/', views.edition_details, name='edition_details'),

    path('borrow/<int:pk>/', views.borrow, name='borrow'),
    path('return/<int:pk>/', views.return_book, name='return'),

    path('authors/add', views.add_author, name='add_author'),
    path('categories/add', views.add_category, name='add_category'),

    path('customers/', views.customers, name='customers'),
    path('customers/add/', views.add_customer, name='add_customer'),
    path('customers/<int:pk>/', views.customer_details, name='customer_details'),

    path('borrow/details/<int:pk>', views.borrow_details, name='borrow_details'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('register/', views.registerPage, name='register')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

