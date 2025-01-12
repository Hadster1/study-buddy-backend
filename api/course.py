# type: ignore
from datetime import datetime as dt
from datetime import timedelta
from my_calendar import Calendar, Event
from fsrs import Scheduler, Card, Rating, ReviewLog
from typing import List
class Course:
    def __init__(self, name, startDate, endDate, program, textbook, topics, scheduler=None, cardList=None, courseConfidence=None):
        self.name = name
        self.startDate = startDate
        self.endDate = endDate
        self.program = program
        self.textbook = textbook
        self.topics = topics
        self.scheduler = Scheduler(maximum_interval= (91 - (dt.now().day - startDate.day)))
        self.cardList = [Card(card_id = i) for i in range(len(topics))]
        self.courseConfidence = courseConfidence

    def addMidterm(midterm: Event, calendar: Calendar):
        calendar.addEvent(midterm)

    def addFinal(final: Event, calendar: Calendar):
        calendar.addEvent(final)

    def removeMidterm(midterm: Event , calendar: Calendar):
        calendar.removeEvent(midterm)

    def removeFinal(final: Event, calendar: Calendar):
        calendar.removeEvent(final)
    
    def getCourseTopics():
        return self.topics
    
    def getTextbook():
        return self.textbook
    
    def addCourseTopic(topic):
        self.topics[topic] = 0.00

    def removeCourseTopic(topic):
        self.topics.pop(topic)

    def getCourseStartDate():
        return self.startDate
    
    def getCourseEndDate():
        return self.endDate
    
    def setCourseStartDate(startDate):
        self.startDate = startDate

    def setCourseEndDate(endDate):
        self.endDate = endDate

    def getCourseConfidence():
        sum = 0
        for topic in self.topics:
            sum += self.topics[topic]
        average = sum / len(self.topics)
        return average
    
    def setTopicConfidence(topic, confidence):
        self.topics[topic] = confidence
    
    def scheduleCard(card: Card):
        rating = Rating.Again
        if (self.topics[topic] < 0.5):
            rating = Rating.Again
        elif (self.topics[topic] >= 0.5 and self.topics[topic] < 0.65):
            rating = Rating.Hard
        elif (self.topics[topic] >= 0.65 and self.topics[topic] < 0.85):
            rating = Rating.Good
        elif (self.topics[topic] >= 0.85):
            rating = Rating.Easy
        card, reviewLog = self.scheduler.schedule(card, rating)
        return card.due
        
