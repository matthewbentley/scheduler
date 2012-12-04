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

class CustomEvent(models.Model):
    event_name = models.CharField(max_length=120)
    event = models.ForeignKey('Event')

class MeetingTime(models.Model):
    meeting_class = models.ForeignKey('Class')
    meeting_event = models.ForeignKey('Event')
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

class CourseEnrollment(models.Model):
    student = models.ForeignKey('Student')
    course = models.ForeignKey('MeetingTime')

class CustomEventEnrollment(models.Model):
    student = models.ForeignKey('Student')
    event = models.ForeignKey('CustomEvent')
