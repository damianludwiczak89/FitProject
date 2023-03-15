from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return f"{self.username}"

class Training(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=600)
    time = models.CharField(max_length=12)
    day = models.CharField(max_length=10)
    calendar_index = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "time": self.time,
            "day": self.day,
            "calendar_index": self.calendar_index
        }
    
class Meal(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=600)
    time = models.CharField(max_length=12)
    day = models.CharField(max_length=10)
    calendar_index = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "time": self.time,
            "day": self.day,
            "calendar_index": self.calendar_index
        }
    
class Cardio(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date= models.DateField()
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.IntegerField(blank=True, null=True)
    speed = models.CharField(max_length=10)
    discipline = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user} {self.discipline} on {self.date}"
    
    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "distance": self.distance,
            "time": self.time,
            "speed": self.speed,
            "discipline": self.discipline
        }
    
class Measurement(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    waist = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    chest = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    thigh = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    arm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date= models.DateField()
    notes = models.CharField(max_length=200, blank=True, null=True)


    def __str__(self):
        return f"Measurements of {self.user}"
    
    def serialize(self):
        return {
            "id": self.id,
            "weight": self.weight,
            "waist": self.waist,
            "chest": self.chest,
            "thigh": self.thigh,
            "arm": self.arm,
            "date": self.date,
            "notes": self.notes
        }