from django.contrib import admin
from .models import *


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'release_date', 'price')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
