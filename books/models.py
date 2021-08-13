from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200, unique=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True)
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)
    date_published = models.DateField()
    book_cover = models.ImageField(default='image-not-found.png', blank=True, null=True)

    def __str__(self):
        return self.title


class BookEdition(models.Model):
    STATUS_CHOICES = (
        ('AVAILABLE', 'AVAILABLE'),
        ('BORROWED', 'BORROWED')
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    ISBN = models.CharField(max_length=10)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='AVAILABLE')

    def __str__(self):
        return "("+str(self.id)+") "+self.book.title+": " + str(self.ISBN)


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    email = models.CharField(max_length=200, unique=True)
    phone = PhoneNumberField()

    def __str__(self):
        return self.first_name + " " + self.last_name


class ReturnReceipt(models.Model):
    STATUS_CHOICES = (
        ('ON-TIME', 'ON-TIME'),
        ('LATE', 'LATE')
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book_edition = models.ForeignKey(BookEdition, on_delete=models.CASCADE)
    date_borrowed = models.DateTimeField()
    date_returned = models.DateTimeField(auto_now_add=True)
    return_status = models.CharField(choices=STATUS_CHOICES, max_length=100)
    damage_status = models.BooleanField(default=False)
    damage_description = models.CharField(blank=True, null=True, max_length=200, default='N/A')
    fine = models.PositiveIntegerField(default=0)


class BorrowReceipt(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    book_edition = models.ForeignKey(BookEdition, on_delete=models.CASCADE)
    date_borrowed = models.DateField(auto_now_add=True)
    date_to_return = models.DateField(blank=True, null=True)

    return_receipt = models.ForeignKey(ReturnReceipt, on_delete=models.PROTECT, blank=True, null=True, default=None)