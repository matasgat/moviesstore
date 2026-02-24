from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

# Create your models here.
class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    def average_rating(self):
        average = self.review_set.aggregate(Avg('rating'))['rating__avg']
        if average is not None:
            return round(average, 1)
        return 0

class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name