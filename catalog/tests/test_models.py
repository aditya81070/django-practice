from django.test import TestCase
#Write your test here
from catalog.models import Author


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # setup non-modifies objects used by all tests
        Author.objects.create(first_name='Aditya',last_name='Agarwal')

    def test_first_name_label(self):
        author=Author.objects.get(id=1)
        field_label=author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label,'first name')

    def test_first_name_max_lenght(self):
        author= Author.objects.get(id=1)
        max_length=author._meta.get_field('first_name').max_length
        self.assertEqual(max_length,100)

    def test_object_name_is_last_name_comma_first_name(self):
        author=Author.objects.get(id=1)
        expected_name='%s, %s' %(author.last_name, author.first_name)
        self.assertEqual(expected_name,str(author))

    def test_get_absolute_url(self):
        author=Author.objects.get(id=1)
        expected_url=author.get_absolute_url()
        self.assertEqual(expected_url,'/catalog/authors/1')