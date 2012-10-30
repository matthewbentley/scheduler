#!/usr/bin/env python

from bs4 import BeautifulSoup
from Models import Class, MeetingTime
import sys

b = BeautifulSoup(open(sys.argv[1]))

classes = b.term.classes.find_all('class')
c_models = []
m_models = []
for c in classes:
    c_num = c.catalognbr.contents
    d = c.subject.contents
    name = c.coursetitle.contents
    desc = c.description.contents
    c_model = Class(class_number=c_num, dept=d, classname=name, description=desc)
    c_models.add(c_model)

    meetings = c.meeting.find_all(meetingdates)
    for meeting in meetings:
        dates = meeting.meetingdates.contents
        times = meeting.daystimes.contents
        room = meeting.room.contents
        s_date = dates.split("-")[0]
        e_date = dates.split("-")[1]
        weekdays = times.split(" ")[0]
        s_time = times.split(" ")[1]
        e_time = times.split("-")[1]
        m_models.add(Meeting(meeting_class = c_model, meeting_date = s_date, meeting_end_date = e_date, meeting_recur_type = weekdays, meeting_location = room, meeting_time = s_time, meeting_end = e_time, meeting_instructore = inst))

for c in c_models:
    c.save()
for m in m_models:
    m.save()
