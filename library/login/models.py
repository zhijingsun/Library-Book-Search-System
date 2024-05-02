from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    birthday = models.DateField(null=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    book_id = models.IntegerField()
    # book = models.ForeignKey('Book', on_delete=models.CASCADE)

    class Meta:
        db_table = 'favorite'
        constraints = [
            models.UniqueConstraint(fields=['user', 'book_id'], name='unique_favorite')
        ]
        # unique_together = ('user', 'book_id')
        # unique_together = ('user', 'book')

class Book(models.Model):
    book_id = models.IntegerField(primary_key=True)
    isbn = models.TextField()
    author = models.TextField()
    title = models.TextField()
    publisher = models.TextField()
    publication_year = models.IntegerField()
    subjects = models.TextField()

    class Meta:
        db_table = 'book'  # 确保这里指定了正确的表名