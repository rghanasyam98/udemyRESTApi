from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator
from django.contrib.auth.models import User

# Create your models here.


class StreamPlatform(models.Model):
    name=models.CharField(max_length=30)
    about=models.CharField(max_length=150)
    website=models.URLField(max_length=100)
    
    def __str__(self):
        return self.name



class WatchList(models.Model):
    platform=models.ForeignKey(StreamPlatform, related_name='watchlist', on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    storyline=models.CharField(max_length=200)
    active=models.BooleanField(default=True)
    avg_rating=models.FloatField(default=0)
    total_rating=models.IntegerField(default=0)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title}"


class Review(models.Model):
    review_user=models.ForeignKey(User,on_delete=models.CASCADE )
    watchlist=models.ForeignKey(WatchList,on_delete=models.CASCADE, related_name='reviews')
    rating=models.PositiveIntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)])
    description=models.CharField(max_length=150)
    active=models.BooleanField( default=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    
    
    def __str__(self) :
        return f"{self.rating} - {self.watchlist.title}"











#model for initial lecture
# class Movie(models.Model):
#     name=models.CharField(max_length=50)
#     description=models.CharField(max_length=200)
#     active=models.BooleanField(default=True)
    
#     def __str__(self):
#         return self.name