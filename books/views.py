from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect

from .filters import BookFilter
from .models import Book, BookEdition, BorrowReceipt, Customer
from .forms import BookForm, BorrowForm, EditionForm, ReturnForm, AuthorForm, CategoryForm\
    , QBorrowReturnForm, CustomerForm, CreateUserForm

import datetime


@login_required()
def home(request):
    books_count = Book.objects.all().count()
    editions_count = BookEdition.objects.all().count()
    books_borrowed = BorrowReceipt.objects.all().filter(return_receipt=None).count()
    due_today = BorrowReceipt.objects.all().filter(date_to_return=datetime.date.today()).count()

    borrow_return_form = QBorrowReturnForm()

    context = {'books_count': books_count, 'editions_count': editions_count, 'borrowed_count': books_borrowed,
               'due_today': due_today, 'renew_form': borrow_return_form}

    if request.method == 'GET':
        borrow_return_form = QBorrowReturnForm(request.GET)

        if borrow_return_form.is_valid():
            book_edition_id = borrow_return_form.cleaned_data.get("book_edition_id")
            book_edition = BookEdition.objects.all().filter(id=book_edition_id)

            if len(book_edition) > 0:
                if book_edition[0].status == 'AVAILABLE':
                    return redirect('borrow', book_edition_id)

                else :
                    return redirect('return', book_edition_id)

    return render(request, 'books/home.html', context)


@login_required()
def books(request):
    book_list = Book.objects.all()
    book_filter = BookFilter(request.GET, queryset=book_list)
    book_list = book_filter.qs

    context = {'books_list': book_list, 'book_filter': book_filter}

    return render(request, 'books/books.html', context)


@login_required()
def customers(request):
    customer_list = Customer.objects.all()

    context = {'customer_list': customer_list}

    return render(request, 'books/customers.html', context)


@login_required()
def book_details(request, pk):
    book = Book.objects.get(id=pk)
    editions = book.bookedition_set.all()

    context = {'book': book, 'editions': editions}
    return render(request, 'books/book.html', context)


@login_required()
def edition_details(request, pk):
    edition = BookEdition.objects.get(id=pk)
    borrow_receipts = BorrowReceipt.objects.filter(book_edition=edition)

    context = {'edition': edition, 'borrow_receipts': borrow_receipts}
    return render(request, 'books/edition_details.html', context)


@login_required()
def customer_details(request, pk):
    customer = Customer.objects.get(id=pk)
    borrowed_books = BorrowReceipt.objects.filter(customer=customer)

    context = {'customer': customer, 'borrowed_books': borrowed_books}

    return render(request, 'books/customer.html', context)


@login_required()
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


@login_required()
def add_author(request):
    form = AuthorForm()

    if request.method == 'POST':
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')

    return render(request, 'books/add_author.html', {'form': form})


@login_required()
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')

    return render(request, 'books/add_category.html', {'form': form})


@login_required()
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


@login_required()
def add_customer(request):
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)

        if form.is_valid():
            customer = form.save()

            return redirect('home')

    context = {'form': form}

    return render(request, 'books/add_customer.html', context)


@login_required()
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


@login_required()
def borrow_details(request, pk):
    borrow_receipt = BorrowReceipt.objects.get(id=pk)

    context = {'borrow_receipt': borrow_receipt}

    return render(request, 'books/borrow_details.html', context)


@login_required()
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


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            return redirect('home')

        else:
            messages.info(request, 'Incorrect Username/Password')

    context = {}

    return render(request, 'books/login.html', context)


@login_required()
def logoutPage(request):
    logout(request)

    return redirect('login')


@login_required()
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Librarian ' + username + ' added.')

            return redirect('login')

    context = {'form': form}

    return render(request, 'books/register.html', context)

