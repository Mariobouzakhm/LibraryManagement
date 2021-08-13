from django.shortcuts import render
from django.shortcuts import redirect

from .models import Book, BookEdition, BorrowReceipt
from .forms import BookForm, BorrowForm, EditionForm, ReturnForm, AuthorForm, CategoryForm

import datetime


def home(request):
    books_count = Book.objects.all().count()
    editions_count = BookEdition.objects.all().count()
    books_borrowed = BorrowReceipt.objects.all().filter(return_receipt=None).count()
    due_today = BorrowReceipt.objects.all().filter(date_to_return=datetime.date.today()).count()

    context = {'books_count': books_count, 'editions_count': editions_count, 'borrowed_count': books_borrowed,
               'due_today': due_today}

    return render(request, 'books/home.html', context)


def books(request):
    book_list = Book.objects.all()

    context = {'books_list': book_list}

    return render(request, 'books/books.html', context)


def book_details(request, pk):
    book = Book.objects.get(id=pk)
    editions = book.bookedition_set.all()

    context = {'book': book, 'editions': editions}
    return render(request, 'books/book.html', context)


def add_book(request):
    form = BookForm()
    context = {
        'form': form
    }

    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('books')

    return render(request, 'books/add_book.html', context)


def add_author(request):
    form = AuthorForm()

    if request.method == 'POST':
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')

    return render(request, 'books/add_author.html', {'form': form})


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')

    return render(request, 'books/add_category.html', {'form': form})


def add_edition(request, pk):
    book = Book.objects.get(id=pk)
    form = EditionForm(initial={'book': book})

    if request.method == 'POST':
        form = EditionForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('book_details', pk=book.id)

    context = {'form': form}

    return render(request, 'books/add_edition.html', context)


def borrow(request, pk):
    edition = BookEdition.objects.get(id=pk)

    if edition.status == 'BORROWED':
        return render(request, 'books/borrow_error.html', {})

    form = BorrowForm(initial={'book_edition': edition, 'date_to_return': datetime.date.today() +
                                                                          datetime.timedelta(days=14)})

    if request.method == 'POST':
        form = BorrowForm(request.POST)

        if form.is_valid():
            form.save()

            edition.status = 'BORROWED'
            edition.save()

            return redirect('home')

    context = {'form': form, 'edition': edition}

    return render(request, 'books/borrow.html', context)


def return_book(request, pk):
    edition = BookEdition.objects.get(id=pk)

    if edition.status == 'AVAILABLE':
        return render(request, 'books/return_error.html', {})

    current_borrow = BorrowReceipt.objects.all().filter(book_edition=edition, return_receipt=None)[0]

    return_status_value = 'LATE' if current_borrow.date_to_return < datetime.date.today() else 'ON-TIME'

    initial_data = {'customer': current_borrow.customer, 'book_edition': edition,
                    'date_borrowed': current_borrow.date_borrowed, 'date_returned': datetime.date.today(),
                    'fine': 0, 'return_status': return_status_value}

    form = ReturnForm(initial=initial_data)

    if request.method == 'POST':
        form = ReturnForm(request.POST, initial=initial_data)

        if form.is_valid():
            return_receipt = form.save()
            current_borrow.return_receipt = return_receipt
            current_borrow.save()

            edition.status = 'AVAILABLE'
            edition.save()

            return redirect('home')

    context = {'edition': edition, 'form': form, 'date_to_return': current_borrow.date_to_return}
    return render(request, 'books/return.html', context)
