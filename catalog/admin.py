from django.contrib import admin
from . import models

# admin.site.register(models.Book)
# admin.site.register(models.Author)
# admin.site.register(models.BookInstance)
admin.site.register(models.Genre)

# Register your models here.

class BookInstanceInline(admin.TabularInline):
    model=models.BookInstance

class BookInline(admin.TabularInline):
    model=models.Book


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name',('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
admin.site.register(models.Author, AuthorAdmin)


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','display_genre')
    inlines = [BookInstanceInline]


@admin.register(models.BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','status','borrower','due_back','id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields':('book','imprint','id')
        }),
        ('Avaiability',{
            'fields':('status','borrower','due_back')
        }),
    )
