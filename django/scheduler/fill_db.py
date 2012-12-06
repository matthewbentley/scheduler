#!/usr/bin/env python

from bs4 import BeautifulSoup
from course_scheduler.models import Class, MeetingTime, Instructor, Instructs, Event
import course_scheduler
import sys
import re

def add_twelve_hours(time):
    time_hour = time.split(":")[0]
    time_minute = time.split(":")[1].split(" ")[0]
    if int(time_hour) != 12:
        time_hour = int(time_hour) + 12
    time = str(time_hour) + ":" + time_minute
    return time

def format_date(date):
    parts = [part.strip() for part in date.split("/")]
    return "-".join([parts[2],parts[0],parts[1]])

def format_times(s_time, e_time):
    if "PM" in e_time:
        e_time = add_twelve_hours(e_time)
        s_hour = s_time.strip().split(":")[0]
        e_hour = e_time.strip().split(":")[0]
        if int(e_hour) - int(s_hour) > 6:
            s_time = add_twelve_hours(s_time)

    elif "PM" in s_time:
        s_time = add_twelve_hours(s_time)

    if "AM" in s_time or "PM" in s_time:
        s_time = s_time.strip().split(" ")[0]

    if "AM" in e_time or "PM" in e_time:
        e_time = e_time.strip().split(" ")[0]

    return (s_time, e_time)

def main():

    xml_file = ""
    with open(sys.argv[1]) as f:
        xml_file += f.read()

    print 'file opened'

    b = BeautifulSoup(xml_file, "lxml")

    print 'file parsed'

    for curr_term in b.find_all('term'):

        classes = curr_term.classes.find_all('class')
        term_name = unicode(curr_term.descr.contents[0])

        for c in classes:
            c_num = c.catalognbr.contents[0]
            d = c.subject.contents[0]
            name = c.coursetitlelong.contents[0]
            try:
                desc = c.description.contents[0]
            except AttributeError:
                try:
                    desc = c.classnotes.contents[0]
                except AttributeError:
                    desc = ""

            try:
                c_num = int(re.search(r'\d+', c_num).group())
            except Exception:
                print c_num
                c_num = int(c_num)
            try:
                d = unicode(d)
                name = unicode(name)
                if len(desc) > 4096:
                    desc = desc[:4095]
                desc = unicode(desc)
                print 'adding:  ' + ' '.join([unicode(c_num), unicode(d), unicode(name), unicode(desc), unicode(term_name)])
            except ValueError,UnicodeEncodeError:
                continue

            c_model = Class(class_number=c_num, dept=d, classname=name, description=desc, term=term_name)
            c_model.save()

            try:
                meetings = c.meetings.find_all('meeting')
            except AttributeError:
                continue

            print 'meetings for this class:'

            for meeting in meetings:
                print meeting
                dates = meeting.meetingdates.contents[0]
                times = meeting.daystimes.contents[0]
                room = unicode(meeting.room.contents[0])
                s_date = dates.split("-")[0].strip()
                e_date = dates.split("-")[1].strip()
                weekdays = times.split(" ")[0]
                try:
                    s_time = times.split(" ")[1].strip()
                    e_time = times.split("-")[1].strip()
                    s_time, e_time = format_times(s_time, e_time)
                    if s_time == "" or e_time == "":
                        continue
                except IndexError:
                    continue

                s_date = format_date(s_date)
                e_date = format_date(e_date)

                print 'adding:  ' + ' '.join([str(s_date), str(e_date), str(weekdays), str(room), str(s_time), str(e_time)])
                m = MeetingTime(meeting_class = c_model, meeting_location = room, start_date = s_date, end_date = e_date, recur_type = weekdays, start_time = s_time, end_time = e_time)
                m.save()

                insts = unicode(meeting.instructor.contents[0])
                for inst_name in insts.split(","):
                    inst, created = Instructor.objects.get_or_create(name=inst_name)
                    instructs = Instructs(instructor=inst, meeting = m)
                    instructs.save()

if __name__ == "__main__":
    main()
