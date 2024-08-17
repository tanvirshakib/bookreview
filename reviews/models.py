from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    CATEGORY_CHOICES = [
    ("Literary Fiction", "Literary Fiction"), 
    ("Historical Fiction", "Historical Fiction"), 
    ("Science Fiction", "Science Fiction"), 
    ("Fantasy", "Fantasy"),
    ("Mystery", "Mystery"), 
    ("Thriller", "Thriller"), 
    ("Romance", "Romance"), 
    ("Horror", "Horror"), 
    ("Biography", "Biography"), 
    ("Memoir", "Memoir"),
    ("Self-Help", "Self-Help"), 
    ("History", "History"), 
    ("Travel", "Travel"), 
    ("True Crime", "True Crime"), 
    ("Science", "Science"), 
    ("Philosophy", "Philosophy"),
    ("Picture Books", "Picture Books"), 
    ("Early Readers", "Early Readers"), 
    ("Middle Grade", "Middle Grade"), 
    ("Young Adult", "Young Adult"),
    ("Textbooks", "Textbooks"), 
    ("Reference", "Reference"), 
    ("Essays", "Essays"), 
    ("Study Guides", "Study Guides"), 
    ("Classic Poetry", "Classic Poetry"),
    ("Contemporary Poetry", "Contemporary Poetry"), 
    ("Anthologies", "Anthologies"), 
    ("Haiku", "Haiku"), 
    ("Plays", "Plays"), 
    ("Screenplays", "Screenplays"),
    ("Manga", "Manga"), 
    ("Comics", "Comics"), 
    ("Graphic Non-Fiction", "Graphic Non-Fiction"), 
    ("Religious Texts", "Religious Texts"), 
    ("Spirituality", "Spirituality"),
    ("Theology", "Theology"), 
    ("Nutrition", "Nutrition"), 
    ("Fitness", "Fitness"), 
    ("Mental Health", "Mental Health"), 
    ("Medical", "Medical"), 
    ("Management", "Management"),
    ("Leadership", "Leadership"), 
    ("Finance", "Finance"), 
    ("Entrepreneurship", "Entrepreneurship"), 
    ("Programming", "Programming"), 
    ("Engineering", "Engineering"),
    ("Artificial Intelligence", "Artificial Intelligence"), 
    ("Cybersecurity", "Cybersecurity"), 
    ("Photography", "Photography"), 
    ("Painting", "Painting"),
    ("Music Theory", "Music Theory"), 
    ("Art History", "Art History"), 
    ("Cooking", "Cooking"), 
    ("Gardening", "Gardening"), 
    ("Knitting", "Knitting"),
    ("Woodworking", "Woodworking"), 
    ("Sports Biography", "Sports Biography"), 
    ("Training Guides", "Training Guides"), 
    ("Adventure", "Adventure")
]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=200, choices=CATEGORY_CHOICES)
    pdf = models.FileField(upload_to='books/pdfs/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='books/covers/', blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    isbn = models.CharField(max_length=13, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        reviews = Review.objects.filter(book=self)
        if reviews.exists():
            return sum(review.rating for review in reviews) / reviews.count()
        return 0


from django.utils import timezone
class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1, choices=[(i, i) for i in range(1, 11)])  # Rating scale of 1 to 10
    review_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Review for {self.book.title} by {self.user.username}'
    
    def is_owner(self, user):
        return self.user == user




from django.db import models
from django.contrib.auth.models import User

class BookClub(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    members = models.ManyToManyField(User, related_name='book_clubs')

    def __str__(self):
        return self.name

class Discussion(models.Model):
    book_club = models.ForeignKey(BookClub, on_delete=models.CASCADE, related_name='discussions')
    topic = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic






class Bookshelf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class BookshelfItem(models.Model):
    bookshelf = models.ForeignKey(Bookshelf, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('bookshelf', 'book')
