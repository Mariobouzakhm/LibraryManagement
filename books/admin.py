from django.contrib import admin
from .models import Category, Author, Book, BookEdition, Customer, BorrowReceipt, ReturnReceipt

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(BookEdition)

admin.site.register(BorrowReceipt)
admin.site.register(ReturnReceipt)

