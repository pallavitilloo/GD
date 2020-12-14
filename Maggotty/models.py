from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import date

@property
def is_upcoming(self):
    today = date.today().strftime('%Y-%m-%d')
    nottoday = self.date.strftime('%Y-%m-%d')
    if  today < nottoday:
        return True
    return False

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)    


    def __str__(self):
        return self.user.username


class Event(models.Model):
    eventName = models.CharField("Event Name", max_length=255, blank=False)
    eventDesc = models.TextField("Event Description", max_length=1024, blank=True, null=True)
    fromDate = models.DateField(blank=False)
    toDate = models.DateField(blank=False)
    startTime = models.TimeField()
    endTime = models.TimeField()
    ticket = models.FloatField("Ticket Price", null=True)
    isApproved = models.BooleanField("Is Approved", default=False)
    createdBy = models.CharField("Created By", max_length=255, editable=False)


    def __str__(self):
        return self.eventName

# added contribute model to store input from "upload content"/ contribute page
class Contribute(models.Model):
    title = models.CharField(max_length=255)
    upload = models.ImageField(upload_to='contribute/')
    description = models.TextField()

    def __str__(self):
        return self.title


class Poll(models.Model):
    question = models.TextField()
    choice_1 = models.CharField(max_length=34)
    choice_2 = models.CharField(max_length=34)

    def __str__(self):
        return self.question


class UserOpinions(models.Model):    
    question_1 = models.CharField(max_length=255, blank=True, null=True)
    question_2 = models.CharField(max_length=255, blank=True, null=True)
    answers_1 =  models.CharField(max_length=255, blank=True, null=True)
    answers_2 =  models.CharField(max_length=255, blank=True, null=True)
    opinion = models.TextField(default="Test Opinion")
    username = models.CharField(max_length=255)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.opinion[:10]
