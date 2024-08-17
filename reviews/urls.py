from django.urls import path
from .views import register, user_login, user_logout, profile, home, book_detail, add_review, edit_review, delete_review, add_book,book_clubs, add_book_club, book_club_detail, add_discussion, bookshelves, add_bookshelf, bookshelf_detail, add_bookshelf_item

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('books/<int:id>/', book_detail, name='book_detail'),
    path('books/<int:id>/add_review/', add_review, name='add_review'),
    path('reviews/<int:review_id>/edit/', edit_review, name='edit_review'),
    path('reviews/<int:review_id>/delete/', delete_review, name='delete_review'),
    path('books/add/', add_book, name='add_book'),
    path('book_clubs/', book_clubs, name='book_clubs'),
    path('book_clubs/add/', add_book_club, name='add_book_club'),
    path('book_clubs/<int:club_id>/', book_club_detail, name='book_club_detail'),
    path('book_clubs/<int:club_id>/add_discussion/', add_discussion, name='add_discussion'),
    path('bookshelves/', bookshelves, name='bookshelves'),
    path('bookshelves/add/', add_bookshelf, name='add_bookshelf'),
    path('bookshelves/<int:bookshelf_id>/', bookshelf_detail, name='bookshelf_detail'),
    path('bookshelves/<int:bookshelf_id>/add_item/', add_bookshelf_item, name='add_bookshelf_item'),
] 