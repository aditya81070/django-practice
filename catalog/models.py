from django.db import models
from django.urls import reverse #used to generate URL's by reversing the URL patterns
import uuid #Require for unique book instances
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Genre(models.Model):
    """
    Model representing a book genre(e.g. Science Fiction, Non Fiction).
    """
    name= models.CharField(max_length= 200, help_text="Enter a book genre (e.g. Science Fiction, Non fiction")

    def __str__(self):
        """
        String for representing the Model Object(in Admin site)
        :return: name of genre
        """
        return self.name



class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book)
    """
    title=models.CharField(max_length=200)
    author= models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have many books
    summary= models.TextField(max_length=1000, help_text="Enter a brief summary of book")
    isbn= models.CharField('ISBN', max_length=13, help_text='13, Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre= models.ManyToManyField(Genre, help_text='Select a genre for this book')
    # ManyToManyField used because genre can contain many books. Books can cover many genres.

    def __str__(self):
        """
        String for representing the Model Object
        :return: title of book
        """
        return self.title

    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this book.
        :return: return url for particular object
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        create a string for the Genre. This is required to display genre to admin page
        :return:
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description='Genre'

class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (ie that can be borrowed from the library).
    """
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book= models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint= models.CharField(max_length=200)
    due_back=models.DateField(null=True, blank=True)
    LOAN_STATUS=(
        ('m','Maintenance'),
        ('o','On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    status=models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')
    borrower=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering=['due_back']
        permissions=(("can_mark_returned","Set book as returned"),)

    def __str__(self):
        return '{0} ({1})'.format(self.id, self.book.title)

    @property
    def is_overdue(self):
        if self.due_back and date.today()> self.due_back:
            return True
        return False


class Author(models.Model):
    """
    Model representing an author
    """
    first_name= models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    date_of_birth=models.DateField(null=True,blank=True)
    date_of_death=models.DateField(null=True, blank=True)

    class Meta:
        ordering=['last_name','first_name']

    def get_absolute_url(self):
        """
        return url to access a particular author instance.
        :return:
        """
        return  reverse('author-detail',args=[str(self.id)])

    def __str__(self):
        return '{0} {1}'.format(self.last_name, self.first_name)