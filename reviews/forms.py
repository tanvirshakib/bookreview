from django import forms
from .models import Review, Book

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text', 'rating']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 11)])
        }

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    published_date = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))

    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'pdf', 'cover_photo', 'published_date', 'isbn', 'language', 'publisher']



from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username")


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")





from django import forms
from .models import BookClub, Discussion, Bookshelf, BookshelfItem

class BookClubForm(forms.ModelForm):
    class Meta:
        model = BookClub
        fields = ['name', 'description']

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['topic', 'message']


class BookshelfForm(forms.ModelForm):
    class Meta:
        model = Bookshelf
        fields = ['name']

class BookshelfItemForm(forms.ModelForm):
    class Meta:
        model = BookshelfItem
        fields = ['book']


