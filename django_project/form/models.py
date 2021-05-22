from django.db import models
from django.db.models import Model
from django import forms
# Create your models here.


class Form(Model):
	first_name=models.CharField(max_length=50)
	last_name=models.CharField(max_length=50)
	dob=models.DateTimeField()
	userid=models.CharField(max_length=50)



class Parent(models.Model):
    name = models.CharField(max_length=255)

class Child(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class Address(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    country = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    address = models.CharField(max_length=255)