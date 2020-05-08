from django.db import models

# Create your models here.


class Person(models.Model):
    first = models.CharField(max_length=30)
    last = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
    	return self.first + ' ' + self.last + ' is ' + str(self.age)