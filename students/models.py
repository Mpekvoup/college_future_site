from django.db import models
from  django.shortcuts import render, get_object_or_404,redirect

class Group(models.Model):
    name = models.CharField(max_length = 100)
    curator = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Club(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField(("Age"), null=True, blank=True)
    group = models.ForeignKey(Group,on_delete = models.CASCADE)
    club = models.ManyToManyField(Club,blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"