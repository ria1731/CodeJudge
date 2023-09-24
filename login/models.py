from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Problem(models.Model):
    problemNumber=models.IntegerField(100)
    problemName=models.CharField(max_length=500)
    problemDifficulty=models.CharField(max_length=10)
    problemDescription=models.CharField(max_length=5000)

class User(models.Model):
    userName=models.CharField(max_length=100)
    password=models.CharField(max_length=200)
    score = models.IntegerField(default=0)

class Submission(models.Model):
    result = models.CharField(max_length=50, default="FAILED")
    problem = models.ForeignKey(Problem, null=True, on_delete=models.SET_NULL)
    langauge = models.CharField(max_length=50, default="Java")
    submission_time = models.DateTimeField(auto_now_add=True, null=True)
    user=models.ForeignKey(User, null=True, on_delete=models.SET_NULL)   


class TestCases(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField()

    def __str__(self):
        return "TC: " + str(self.id) + " for problem :" + str(self.problem)    
      