from django.db import models
from django.urls import reverse
from datetime import date

# Create your models here.
class Creature(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.name
    
    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(FEEDTIME)


MEALS = (
    ('L', 'Light'),
    ('W', 'Worms'),
    ('M', 'Marine Snow'),
    ('P', 'Phytoplankton')
)

FEEDTIME = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)



class Feeding(models.Model):
    date = models.DateField()
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
    )
    feedtime = models.CharField(
        max_length=1,
        choices=FEEDTIME,
        default=FEEDTIME[0][0]
    )

    creature = models.ForeignKey(Creature, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_meal_display()} at {self.get_feedtime_display()} on {self.date}'

    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    creature = models.ForeignKey(Creature, on_delete=models.CASCADE)

    def __str__(self):
        return f'Photo for creature_id: {self.creature_id} @{self.url}'