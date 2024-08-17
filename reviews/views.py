from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm, ReviewForm, BookForm
from .models import Book, Review
from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Book, Review
from .serializers import UserSerializer, BookSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import viewsets, permissions

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to the home page after login
    else:
        form = CustomUserCreationForm()
    return render(request, 'reviews/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                user = User.objects.get(username=username_or_email)

            if user.check_password(password):
                login(request, user)
                return redirect('home')
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'reviews/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

from django.db.models import Max

def home(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    if query:
        books = Book.objects.filter(title__icontains=query)
    elif category:
        books = Book.objects.filter(category=category)
    else:
        books = Book.objects.all()

    # Recently reviewed books
    recent_books = Book.objects.filter(reviews__isnull=False).distinct().annotate(last_review_date=Max('reviews__created_at')).order_by('-last_review_date')[:6]

    categories = Book.CATEGORY_CHOICES
    return render(request, 'reviews/home.html', {
        'books': books,
        'recent_books': recent_books,
        'categories': categories
    })


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    reviews = Review.objects.filter(book=book)
    form = ReviewForm()
    return render(request, 'reviews/book_detail.html', {'book': book, 'reviews': reviews, 'form': form})


@login_required
def add_review(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', id=book.id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/add_review.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'reviews/profile.html', {'form': form, 'reviews': reviews})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('book_detail', id=review.book.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'reviews/edit_review.html', {'form': form, 'review': review})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    book_id = review.book.id
    if request.method == 'POST':
        review.delete()
        return redirect('book_detail', id=book_id)
    return render(request, 'reviews/delete_review.html', {'review': review})


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm()  # Initialize form here# Render the form regardless of the request method
        return render(request, 'reviews/add_book.html', {'form': form})




from django.shortcuts import render, get_object_or_404, redirect
from .models import BookClub, Discussion
from .forms import BookClubForm, DiscussionForm
from django.contrib.auth.decorators import login_required

def book_clubs(request):
    clubs = BookClub.objects.all()
    return render(request, 'reviews/book_clubs.html', {'clubs': clubs})

@login_required
def add_book_club(request):
    if request.method == 'POST':
        form = BookClubForm(request.POST)
        if form.is_valid():
            club = form.save()
            club.members.add(request.user)  # Add the creator as a member
            return redirect('book_clubs')
    else:
        form = BookClubForm()
    return render(request, 'reviews/add_book_club.html', {'form': form})

def book_club_detail(request, club_id):
    club = get_object_or_404(BookClub, id=club_id)
    discussions = Discussion.objects.filter(book_club=club)
    return render(request, 'reviews/book_club_detail.html', {'club': club, 'discussions': discussions})

@login_required
def add_discussion(request, club_id):
    club = get_object_or_404(BookClub, id=club_id)
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.book_club = club
            discussion.user = request.user
            discussion.save()
            return redirect('book_club_detail', club_id=club.id)
    else:
        form = DiscussionForm()
    return render(request, 'reviews/add_discussion.html', {'form': form, 'club': club})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Bookshelf, BookshelfItem, Book
from .forms import BookshelfForm, BookshelfItemForm

@login_required
def bookshelves(request):
    user_bookshelves = Bookshelf.objects.filter(user=request.user)
    return render(request, 'reviews/bookshelves.html', {'bookshelves': user_bookshelves})

@login_required
def add_bookshelf(request):
    if request.method == 'POST':
        form = BookshelfForm(request.POST)
        if form.is_valid():
            bookshelf = form.save(commit=False)
            bookshelf.user = request.user
            bookshelf.save()
            return redirect('bookshelves')
    else:
        form = BookshelfForm()
    return render(request, 'reviews/add_bookshelf.html', {'form': form})

@login_required
def bookshelf_detail(request, bookshelf_id):
    bookshelf = get_object_or_404(Bookshelf, id=bookshelf_id, user=request.user)
    items = bookshelf.items.all()
    return render(request, 'reviews/bookshelf_detail.html', {'bookshelf': bookshelf, 'items': items})

@login_required
def add_bookshelf_item(request, bookshelf_id):
    bookshelf = get_object_or_404(Bookshelf, id=bookshelf_id, user=request.user)
    if request.method == 'POST':
        form = BookshelfItemForm(request.POST)
        if form.is_valid():
            bookshelf_item = form.save(commit=False)
            bookshelf_item.bookshelf = bookshelf
            bookshelf_item.save()
            return redirect('bookshelf_detail', bookshelf_id=bookshelf_id)
    else:
        form = BookshelfItemForm()
    return render(request, 'reviews/add_bookshelf_item.html', {'form': form, 'bookshelf': bookshelf})

