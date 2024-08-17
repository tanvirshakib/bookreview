from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book, Review

class BookTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book = Book.objects.create(title='Test Book', author='Test Author', category='Science Fiction')

    def test_book_creation(self):
        self.assertEqual(self.book.title, 'Test Book')
        self.assertEqual(self.book.author, 'Test Author')
        self.assertEqual(self.book.category, 'Science Fiction')

class ReviewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.book = Book.objects.create(title='Test Book', author='Test Author', category='Science Fiction')
        self.review = Review.objects.create(book=self.book, user=self.user, rating=5, review_text='Great book!')

    def test_review_creation(self):
        self.assertEqual(self.review.book.title, 'Test Book')
        self.assertEqual(self.review.user.username, 'testuser')
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.review_text, 'Great book!')

    def test_user_reviews(self):
        reviews = Review.objects.filter(user=self.user)
        self.assertEqual(reviews.count(), 1)
        self.assertEqual(reviews[0].review_text, 'Great book!')
