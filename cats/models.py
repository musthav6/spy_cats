from django.db import models

import requests
from django.core.exceptions import ValidationError



def validate_cat_breed(breed):
    response = requests.get("https://api.thecatapi.com/v1/breeds")
    breeds = [b['name'].lower() for b in response.json()]
    if breed.lower() not in breeds:
        raise ValidationError(f"{breed} is not a valid cat breed.")



class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    breed = models.CharField(max_length=50, validators=[validate_cat_breed])
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Target(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Mission(models.Model):
    spy_cat = models.OneToOneField(SpyCat, on_delete=models.CASCADE, related_name="mission")
    targets = models.ManyToManyField(Target)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission for {self.spy_cat.name}"


