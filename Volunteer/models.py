from django.db import models
import uuid

# Create your models here.

# Mosque Admin
class Admin(models.Model):
    adminid = models.CharField(max_length=10, primary_key=True)
    name = models.TextField(max_length=100)
    password = models.TextField(max_length=100)
    position = models.TextField(max_length=100)
    contactno = models.TextField(max_length=20)
    email = models.EmailField(max_length=100)

# Mosque Committee
class Committee(models.Model):
    committeeid = models.CharField(max_length=10, primary_key=True)
    name = models.TextField(max_length=100)
    password = models.TextField(max_length=100)
    position = models.TextField(max_length=100)
    contactno = models.TextField(max_length=20)
    email = models.EmailField(max_length=100)
    role = models.TextField(max_length=50)

# Event
class Event(models.Model):
    eventid = models.CharField(max_length=10, primary_key=True)
    eventname = models.TextField(max_length=100)
    eventdate = models.DateField()
    tasks = models.TextField()  # You can create a separate Task model if needed
    volcapacity = models.IntegerField(default=10)
    token = models.TextField(max_length=200)
    created_by = models.ForeignKey('Committee', on_delete=models.SET_NULL, null=True)

# Volunteer
class Volunteer(models.Model):
    volunteerid = models.CharField(max_length=10, primary_key=True)
    name = models.TextField(max_length=100)
    password = models.TextField(max_length=100)
    age = models.IntegerField()
    gender = models.TextField(max_length=10)
    contactno = models.TextField(max_length=20)
    email = models.EmailField(max_length=100)
    address = models.TextField(max_length=200)
    skills = models.TextField()  


class TaskApplication(models.Model):
    applicationid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    volunteerid = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    eventid = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    taskid = models.CharField(max_length=10)  
    status = models.TextField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    attendance = models.BooleanField(default=False)
    performancerating = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  
    tokensearned = models.TextField(max_length=100, default="", blank=True)