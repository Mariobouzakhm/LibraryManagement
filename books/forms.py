from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms import DateInput, ModelMultipleChoiceField, CheckboxSelectMultiple
from django import forms

from django.contrib.auth.models import User

from .models import Customer, Book, Category, BorrowReceipt, BookEdition, ReturnReceipt, Author


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class DatePicker(DateInput):
    input_type = 'date'


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

        widgets = {
            'date_published': DatePicker()
        }

    categories = ModelMultipleChoiceField(
        queryset= Category.objects.all(),
        widget= CheckboxSelectMultiple
    )


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

        widgets = {
            'date_of_birth': DatePicker()
        }


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

        widgets = {
            'date_of_birth': DatePicker()
        }


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class EditionForm(ModelForm):
    class Meta:
        model = BookEdition
        fields = '__all__'
        exclude = ['status']


class QBorrowReturnForm(forms.Form):
    book_edition_id = forms.IntegerField(label='Quick Borrow/Return: ', min_value=0,
                                         widget=forms.TextInput(attrs={'placeholder': 'Book Edition #'}))


class BorrowForm(ModelForm):
    class Meta:
        model = BorrowReceipt
        fields = '__all__'
        exclude = ['return_receipt']

        widgets = {
            'date_to_return': DatePicker()
        }


class ReturnForm(ModelForm):
    STATUS_CHOICES = (
        ('ON-TIME', 'ON-TIME'),
        ('LATE', 'LATE')
    )

    class Meta:
        model = ReturnReceipt
        fields = '__all__'

    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), widget=forms.Select, disabled=True,
                                      required=False)
    book_edition = forms.ModelChoiceField(queryset=BookEdition.objects.all(), widget=forms.Select, disabled=True,
                                          required=False)
    date_borrowed = forms.DateField(widget=DateInput, disabled=True, required=False)
    date_returned = forms.DateField(widget=DateInput, disabled=True, required=False)
    damage_description = forms.CharField(required=True, initial='N/A')
    return_status = forms.ChoiceField(choices=STATUS_CHOICES, disabled=True, required=False)
