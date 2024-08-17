from django.contrib import admin
from .models import Book, Review

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'published_date', 'isbn', 'language', 'publisher')
    search_fields = ('title', 'author', 'isbn', 'language', 'publisher')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'review_text')
    search_fields = ('book__title', 'user__username', 'rating')

