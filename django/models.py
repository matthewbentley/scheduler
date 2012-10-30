from django.db import models

class Class(models.Model):
    class_number = models.IntegerField()
    dept = models.CharField(max_length=10)
    classname = models.CharField(max_length=120)
    instructor = models.CharField(max_length = 30)
    description = models.CharField(max_length = 4096)

class MeetingTime(models.Model):
    meeting_class = models.ForeignKey('Class')
    meeting_time = models.TimeField()
    meeting_end = models.TimeField()
    meeting_date = models.DateField()
    meeting_end_date = models.DateField()
    meeting_recur_type = models.CharField(max_length=7)
    meeting_location = models.CharField(max_length=50)


