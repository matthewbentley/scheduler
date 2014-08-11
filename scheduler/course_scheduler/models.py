from django.db import models

class Class(models.Model):
    class_number = models.IntegerField()
    dept = models.CharField(max_length=10)
    classname = models.CharField(max_length=350)
    description = models.CharField(max_length = 4096)
    term = models.ForeignKey('Term')

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
    case_id = models.CharField(max_length=7, primary_key=True)
    name = models.CharField(max_length = 20)

class Schedule(models.Model):
    is_shared = models.BooleanField(default=False)
    student = models.ForeignKey('Student')
    term = models.ForeignKey('Term')

class Term(models.Model):
    term_id = models.IntegerField(primary_key=True)
    term_year = models.IntegerField()
    term_semester = models.CharField(max_length=6)

class Enrollment(models.Model):
    schedule = models.ForeignKey('Schedule')
    event = models.ForeignKey('Event')

class Shares(models.Model):
    share_id = models.CharField(max_length=18, primary_key=True)
    schedule = models.ForeignKey('Schedule')
