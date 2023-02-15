from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse

class Author (models.Model):
    ratingAuthor = models.IntegerField(default=0)
    authorUser = models.OneToOneField(User, on_delete = models.CASCADE,)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')
        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')
        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser.username}'


class Category(models.Model):
    name = models.CharField(max_length=38,unique=True)
    description = models.TextField()
    subscribers = models.ManyToManyField(User,related_name= 'categories')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class News (models.Model):
    ARTICLE ='AR'
    NEW = 'NW'
    CATEGORY_CHOICES = (
        (ARTICLE ,'Статья'),
        (NEW ,'Новость'),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=34)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)
    dateCreation = models.DateTimeField(auto_now_add=True)
    categoryType = models.CharField(max_length=2,choices=CATEGORY_CHOICES,default=ARTICLE)
    category = models.ManyToManyField(Category)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.title} :{self.text}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def preview(self):
        return f'{self.text[:124]}...'


class Comment(models.Model):
    commentPost = models.ForeignKey(News, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateTimeCreation = models.DateTimeField(auto_now_add=True)
    dateCreation = models.DateField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text}'











