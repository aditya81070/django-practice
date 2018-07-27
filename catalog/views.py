from django.shortcuts import render, get_object_or_404
from .models import Book, BookInstance, Author, Genre
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
import datetime
from django.forms import ModelForm
from .forms import RenewBookForm
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import  ValidationError


# Create your views here.
def index(request):
    """
    View function for home page of site
    :param request:
    :return:
    """
    num_books=Book.objects.count()
    num_instances=BookInstance.objects.count()
    #Available books(status='a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()
    num_genres=Genre.objects.count()
    num_programming_books=Book.objects.filter(summary__icontains='program').count()
    num_visits= request.session.get('num_visits',0)
    request.session['num_visits']=num_visits+1
    session_keys=request.session.keys()
    context={
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_genres':num_genres,
        'num_programming_books':num_programming_books,
        'num_visits': num_visits,
        'session_keys': session_keys,
    }
    return render(request,'index.html',context)


class BookListView(generic.ListView):
    model = Book


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 4

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class BorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/borrowed_books_list.html'
    permission_required = ('catalog.can_mark_returned',)
    paginate_by = 10

    def get_queryset(self):
        bookinstList=BookInstance.objects.filter()
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request,pk):
    book_inst=get_object_or_404(BookInstance, pk=pk)
    if request.method=='POST':
        form= RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back=form.cleaned_data['renewal_date']
            book_inst.save()
            return HttpResponseRedirect(reverse('borrowed-books'))
    else:
        proposed_renewal_date=datetime.date.today()+datetime.timedelta(weeks=3)
        form=RenewBookForm(initial={'renewal_date': proposed_renewal_date,})
    context={
        'form': form,
        'bookinst': book_inst,
    }
    return  render(request,'catalog/book_renew_librarian.html',context)

# class RenewBookModel(ModelForm):
#     def clean_due_back(self):
#         data = self.cleaned_data['due_back']
#
#         # Check date is not in past.
#         if data < datetime.date.today():
#             raise ValidationError(_('Invalid date - renewal in past'))
#
#         # Check date is in range librarian allowed to change (+4 weeks)
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
#
#         # Remember to always return the cleaned data.
#         return data
#     class Meta:
#         model = BookInstance
#         fields=['due_back']
#         labels={'due_back': _('Renewal Date'),}
#         help_texts={'due_back':_('Enter a date between now and 4 weeks(default is 3 weeks'),}

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death':'05/01/2018',}
    permission_required = 'catalog.can_add_author'




class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth','date_of_death']
    permission_required = 'catalog.can_update_author'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_delete_author'

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    permission_required = 'catalog.can_add_book'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title','author','summary','isbn','genre']
    permission_required = 'catalog.can_update_book'

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_delete_book'
