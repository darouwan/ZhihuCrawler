from django.db import models

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10)
    followers = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    thanks = models.IntegerField(default=0)
    time = models.DateTimeField('collected date')
    user_id = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class Candidates(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name