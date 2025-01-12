# type: ignore
from datetime import datetime as dt
from datetime import timedelta
class Event:
    name = ''
    location = ''
    startDate = dt.now()
    endDate = dt.now()
    # Daily, Weekly, Bi-Weekly, Monthly, Yearly
    recurrence = ''
    course = ''
    isMultiDay = False
    color = ''

    def __init__(self, name, startDate, endDate, location, recurrence, course=None, isMultiDay=None, color=None):
        self.name = name
        self.startDate = startDate
        self.endDate = endDate
        self.location = location
        self.recurrence = recurrence
        self.course = course
        self.isMultiDay = isMultiDay
        self.color = color

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
        
    def isMultiDay(self):
        return self.isMultiDay
    
    def getColor():
        return self.color
    
    def setColor(color):
        self.color = color

class Day:
    day = dt.now().day
    events = []  # List of events

    def __init__(self, day):
        self.day = day

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
    days = []
    numDays = 31

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
    year = dt.now().year
    monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months = []

    def __init__(self, year):
        self.year = year
        self.months = [Month(days) for days in self.monthDays]
        if self.isLeapYear():
            self.monthDays[1] = 29

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
    degreeDuration = 4
    startDate = dt.now()
    endDate = dt.now() + timedelta(days=365 * degreeDuration)
    studyYears = []

    def __init__(self, startDate, endDate, degreeDuration):
        self.startDate = startDate
        self.endDate = endDate
        self.degreeDuration = degreeDuration
        self.studyYears = [Year(year) for year in range(startDate.year, endDate.year + 1)]

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
            currentDate = event.getStartDate()
            while currentDate <= self.endDate:
                for y in self.studyYears:
                    for m in y.getMonths():
                        for d in m.getDays():
                            if (currentDate.day == d.getDay()
                                    and currentDate.month == y.getMonths().index(m) + 1
                                    and currentDate.year == y.getYear()):
                                d.addEvent(event)
                currentDate += timedelta(days=1)
        elif (event.getRecurrence() == 'Weekly'):
            currentDate = event.getStartDate()
            while (currentDate <= self.endDate):
                for y in self.studyYears:
                    for m in y.getMonths():
                        for d in m.getDays():
                            if (currentDate.day == d.getDay()
                                    and currentDate.month == y.getMonths().index(m) + 1
                                    and currentDate.year == y.getYear()):
                                d.addEvent(event)
                currentDate += timedelta(days=7)
        elif (event.getRecurrence() == 'Bi-Weekly'):
            currentDate = event.getStartDate()
            while (currentDate <= self.endDate):
                for y in self.studyYears:
                    for m in y.getMonths():
                        for d in m.getDays():
                            if (currentDate.day == d.getDay()
                                    and currentDate.month == y.getMonths().index(m) + 1
                                    and currentDate.year == y.getYear()):
                                d.addEvent(event)
                currentDate += timedelta(days=14)
        elif (event.getRecurrence() == 'Monthly'):
            currentDate = event.getStartDate()
            while (currentDate <= self.endDate):
                for y in self.studyYears:
                    for m in y.getMonths():
                        for d in m.getDays():
                            if (currentDate.day == d.getDay()
                                    and currentDate.month == y.getMonths().index(m) + 1
                                    and currentDate.year == y.getYear()):
                                d.addEvent(event)
                currentDate += timedelta(days=30)
        elif (event.getRecurrence() == 'Yearly'):
            currentDate = event.getStartDate()
            while (currentDate <= self.endDate):
                for y in self.studyYears:
                    for m in y.getMonths():
                        for d in m.getDays():
                            if (currentDate.day == d.getDay()
                                    and currentDate.month == y.getMonths().index(m) + 1
                                    and currentDate.year == y.getYear()):
                                d.addEvent(event)
                currentDate += timedelta(days=365)
        elif (event.getRecurrence() == 'Once'):
            for i in self.studyYears:
                if i.getYear() == event.getStartDate().year:
                    yearIndex = self.studyYears.index(i)
            monthIndex = event.getStartDate().month + 1
            dayIndex = event.getStartDate().day
            self.studyYears[yearIndex].getMonths()[monthIndex].getDays()[dayIndex].addEvent(event)