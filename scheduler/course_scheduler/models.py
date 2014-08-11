from django.db import models

class Class(models.Model):
    class_number = models.IntegerField()
    dept = models.CharField(max_length=10)
    classname = models.CharField(max_length=350)
    description = models.CharField(max_length = 4096)
    term = models.CharField(max_length = 30)

class Event(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    recur_type = models.CharField(max_length=12)

class CustomEvent(Event):
    event_name = models.CharField(max_length=120)
    location = models.CharField(max_length=50)

class MeetingTime(Event):
    meeting_class = models.ForeignKey('Class')
    meeting_location = models.CharField(max_length=50)

class Instructor(models.Model):
    email = models.CharField(max_length=10)
    name = models.CharField(max_length = 50, primary_key=True)
    office = models.CharField(max_length = 15)

class Instructs(models.Model):
    instructor = models.ForeignKey('Instructor')
    meeting = models.ForeignKey('MeetingTime')

class Student(models.Model):
    case_id = models.CharField(max_length=6, primary_key=True)

class Enrollment(models.Model):
    student = models.ForeignKey('Student')
    event = models.ForeignKey('Event')

class PublicSchedule(models.Model):
    student = models.ForeignKey('Student')
    schedule_string = models.CharField(max_length=18, primary_key=True)

class Shares(models.Model):
    shareid = models.IntegerField()
    event = models.ForeignKey('Event')
