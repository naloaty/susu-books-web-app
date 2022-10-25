from django.db import models
from django.urls import reverse


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"[{self.pk}] {self.first_name} {self.last_name}"

    def get_edit_url(self):
        return reverse('author_edit', kwargs={'author_id': self.pk})

    def get_delete_url(self):
        return reverse('author_delete', kwargs={'author_id': self.pk})

    class Meta:
        ordering = ['last_name', 'first_name']


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author)
    release_date = models.DateField()
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f"[{self.pk}] {self.title}"

    def get_edit_url(self):
        return reverse('book_edit', kwargs={'book_id': self.pk})

    def get_delete_url(self):
        return reverse('book_delete', kwargs={'book_id': self.pk})

    class Meta:
        ordering = ['title']
