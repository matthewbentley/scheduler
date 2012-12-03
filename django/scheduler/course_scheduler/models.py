from django.db import models

class Class(models.Model):
    class_number = models.IntegerField()
    dept = models.CharField(max_length=10)
    classname = models.CharField(max_length=350)
    description = models.CharField(max_length = 4096)
    term = models.CharField(max_length = 30)

class MeetingTime(models.Model):
    meeting_class = models.ForeignKey('Class')
    meeting_time = models.TimeField()
    meeting_end = models.TimeField()
    meeting_date = models.DateField()
    meeting_end_date = models.DateField()
    meeting_recur_type = models.CharField(max_length=12)
    meeting_location = models.CharField(max_length=50)


class Instructor(models.Model):
    email = models.CharField(max_length=10)
    name = models.CharField(max_length = 50)
    office = models.CharField(max_length = 15)

class Instructs(models.Model):
    instructor = models.ForeignKey('Instructor')
    meeting = models.ForeignKey('MeetingTime')

class Student(models.Model):
    case_id = models.CharField(max_length=6)

class Enrollment(models.Model):
    student = models.ForeignKey('Student')
    course = models.ForeignKey('Class')
