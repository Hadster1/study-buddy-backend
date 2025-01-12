# type: ignore
from datetime import datetime as dt
from datetime import timedelta
import json

class Event:
    def __init__(self, event_id, name, startDate, endDate, location, recurrence, course=None, isMultiDay=None, color=None):
        self.event_id = event_id
        self.name = name
        self.startDate = startDate
        self.endDate = endDate
        self.location = location
        self.recurrence = recurrence
        self.course = course
        self.isMultiDay = isMultiDay
        self.color = color

    def getEventId(self):
        return self.event_id
    
    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getStartDate(self):
        return self.startDate
    
    def setStartDate(self, startDate):
        self.startDate = startDate

    def getEndDate(self):
        return self.endDate
    
    def setEndDate(self, endDate):
        self.endDate = endDate

    def getLocation(self):
        return self.location

    def setLocation(self, location):
        self.location = location

    def getRecurrence(self):
        return self.recurrence

    def setRecurrence(self, recurrence):
        self.recurrence = recurrence

    def getCourse(self):
        return self.course
    
    def setCourse(self, course):
        self.course = course
    
    def setMultiDay(self, isMultiDay):
        self.isMultiDay = isMultiDay

    def getIsMultiDay(self):
        return self.isMultiDay
    
    def getColor(self):
        return self.color
    
    def setColor(color):
        self.color = color

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "name": self.name,
            "startDate": self.startDate.strftime('%Y-%m-%d %H:%M'),
            "endDate": self.endDate.strftime('%Y-%m-%d %H:%M'),
            "location": self.location,
            "recurrence": self.recurrence,
            "course": self.course,
            "isMultiDay": self.isMultiDay,
            "color": self.color
        }

class Day:
    def __init__(self, day):
        self.day = day
        self.events = []

    def getDay(self):
        return self.day

    def setDay(self, day):
        self.day = day

    def getEvents(self):
        return self.events

    def addEvent(self, event):
        self.events.append(event)

    def removeEvent(self, event):
        self.events.remove(event)
    
    def printEvents(self):
        for event in self.events:
            print(event.getName())

class Month:
    def __init__(self, numDays):
        self.days = [Day(i) for i in range(1, numDays + 1)]
        self.numDays = numDays

    def getDays(self):
        return self.days

    def updateDays(self, days):
        self.days = days

    def printDays(self):
        for day in self.days:
            print(day.getDay())

class Year:
    monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    def __init__(self, year):
        self.year = year
        if self.isLeapYear():
            self.monthDays[1] = 29
        self.months = [Month(days) for days in self.monthDays]

    def getYear(self):
        return self.year

    def setYear(self, year):
        self.year = year

    def getMonths(self):
        return self.months

    def updateMonths(self, months):
        self.months = months

    def isLeapYear(self):
        return self.year % 4 == 0 and (self.year % 100 != 0 or self.year % 400 == 0)


class Calendar:
    def __init__(self, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate
        self.degreeDuration = endDate - startDate
        self.studyYears = [Year(year, ) for year in range(startDate.year, endDate.year + 1)]

    def getStartDate(self):
        return self.startDate
    
    def setStartDate(self, startDate):
        self.startDate = startDate

    def setEndDate(self, endDate):
        self.endDate = endDate

    def getEndDate(self):
        return self.endDate
    
    def getStudyYears(self):
        return self.studyYears
    
    def getStudyYear(self, year):
        for y in self.studyYears:
            if y.getYear() == year:
                return y
    def removeEvent(self, event, seriesOption):
        if (seriesOption == 'All'):
            for y in self.studyYears:
                for m in y.getMonths():
                    for d in m.getDays():
                        if event in d.getEvents():
                            d.removeEvent(event)
        elif (seriesOption == 'This'):
            for y in self.studyYears:
                for m in y.getMonths():
                    for d in m.getDays():
                        if (event in d.getEvents() and 
                            event.getStartDate().day == d.getDay() and 
                            y.getMonths().index(m) + 1 == event.getStartDate().month and 
                            y.getYear() == event.getStartDate().year):
                            d.removeEvent(event)
    def addEvent(self, event):
        if (event.getRecurrence() == 'Daily'):
            start_date = event.startDate
            end_date = event.endDate
            current_date = start_date

            while current_date <= end_date:
                self.getStudyYear(current_date.year).getMonths()[current_date.month - 1].getDays()[current_date.day - 1].addEvent(Event(event.getEventId(), event.getName(), current_date, dt(current_date.year, current_date.month, current_date.day, end_date.hour, end_date.minute), event.getLocation(), event.getRecurrence(), event.getCourse(), event.getIsMultiDay(), event.getColor()))
                current_date += timedelta(days=1)
        elif (event.getRecurrence() == 'Weekly'):
            start_date = event.startDate
            end_date = event.endDate
            current_date = start_date

            while current_date <= end_date:
                self.getStudyYear(current_date.year).getMonths()[current_date.month - 1].getDays()[current_date.day - 1].addEvent(Event(event.getEventId(), event.getName(), current_date, dt(current_date.year, current_date.month, current_date.day, end_date.hour, end_date.minute), event.getLocation(), event.getRecurrence(), event.getCourse(), event.getIsMultiDay(), event.getColor()))
                current_date += timedelta(days=7)
        elif (event.getRecurrence() == 'Bi-Weekly'):
            start_date = event.startDate
            end_date = event.endDate
            current_date = start_date

            while current_date <= end_date:
                self.getStudyYear(current_date.year).getMonths()[current_date.month - 1].getDays()[current_date.day - 1].addEvent(Event(event.getEventId(), event.getName(), current_date, dt(current_date.year, current_date.month, current_date.day, end_date.hour, end_date.minute), event.getLocation(), event.getRecurrence(), event.getCourse(), event.getIsMultiDay(), event.getColor()))
                current_date += timedelta(days=14)
        elif (event.getRecurrence() == 'Monthly'):
            start_date = event.startDate
            end_date = event.endDate
            current_date = start_date

            while current_date <= end_date:
                self.getStudyYear(current_date.year).getMonths()[current_date.month - 1].getDays()[current_date.day - 1].addEvent(Event(event.getEventId(), event.getName(), current_date, dt(current_date.year, current_date.month, current_date.day, end_date.hour, end_date.minute), event.getLocation(), event.getRecurrence(), event.getCourse(), event.getIsMultiDay(), event.getColor()))
                next_month = current_date.month + 1 if current_date.month < 12 else 1
                next_year = current_date.year if current_date.month < 12 else current_date.year + 1
                current_date = dt(next_year, next_month, current_date.day)
        elif (event.getRecurrence() == 'Yearly'):
            start_date = event.startDate
            end_date = event.endDate
            current_date = start_date

            while current_date <= end_date:
                self.getStudyYear(current_date.year).getMonths()[current_date.month - 1].getDays()[current_date.day - 1].addEvent(Event(event.getEventId(), event.getName(), current_date, dt(current_date.year, current_date.month, current_date.day, end_date.hour, end_date.minute), event.getLocation(), event.getRecurrence(), event.getCourse(), event.getIsMultiDay(), event.getColor()))
                current_date += timedelta(days=365)
        elif (event.getRecurrence() == 'Once'):
            for i in self.studyYears:
                if i.getYear() == event.getStartDate().year:
                    yearIndex = self.studyYears.index(i)
            monthIndex = event.getStartDate().month + 1
            dayIndex = event.getStartDate().day
            self.studyYears[yearIndex].getMonths()[monthIndex].getDays()[dayIndex].addEvent(event)
    def to_json(self):
        events = []
        for year in self.studyYears:
            for month in year.getMonths():
                for day in month.getDays():
                    for event in day.getEvents():
                        if event is not None:
                            events.append(event.to_dict())
        return json.dumps(events, indent=4)
    
    def to_json_unique(self):
        events = []
        seen_ids = set()
        for year in self.studyYears:
            for month in year.getMonths():
                for day in month.getDays():
                    for event in day.getEvents():
                        if event is not None and event.getEventId() not in seen_ids:
                            seen_ids.add(event.getEventId())
                            events.append(event.to_dict())
        return json.dumps(events, indent=4)
    
# if __name__ == '__main__':
#     startDate = dt(2021, 1, 1)
#     endDate = dt(2025, 12, 31)
#     calendar = Calendar(startDate, endDate)
#     event = Event(1,"Meeting", dt(2021, 1, 1, 10, 0), dt(2024, 2, 29, 12, 0), "Office", "Yearly", "CS 361", False, "Red")
#     calendar.addEvent(event)
#     event1 = Event(2,"Meeting", dt(2021, 1, 1, 11, 0), dt(2021, 2, 28, 13, 0), "Office Hours", "Daily", "CS 361", False, "Red")
#     calendar.addEvent(event1)
#     print(calendar.to_json_unique())
