import re
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from Maggotty.forms import CreateEventForm, ContactUsForm, FeedbackForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect, request
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Maggotty.models import Event, Order
from django.db import models
from django.views.generic import ListView, DetailView
from datetime import date
from django.conf import settings
from django.core.mail import send_mail
from Maggotty.models import Contribute, Poll, UserOpinions


def paystatus(request):        
    current_user = request.user    
    Order.objects.filter(username=current_user.username, ifPaid=False).update(ifPaid=True)    
    return render(request, "Maggotty/paystatus.html")

def home(request):
    return render(request, "Maggotty/home.html")

def about(request):
    return render(request, "Maggotty/about.html")

def donate(request):
    return render(request, "Maggotty/donate.html")

def faq(request):
    return render(request, "Maggotty/faq.html")

def history(request):
    return render(request, "Maggotty/history.html")

def mission(request):
    return render(request, "Maggotty/mission.html")

def news(request):
    return render(request, "Maggotty/news.html")

# def register(request):
#     registered = False
#     if request.method == 'POST':
#         user_form = RegisterForm(data=request.POST)
#         profile_form = UserProfileInfoForm(data=request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = user
#             messages.success(request, f'✔️ User account created successfully for {user}. You can login and access your account now!')
#             subject = "Registration successful!"
#             message = settings.REGISTRATION_EMAIL_BODY
#             email_from = settings.EMAIL_HOST_USER 
#             recipient_list = [user.email] 
#             send_mail(subject, message, email_from, recipient_list) 

#             return redirect('home')
#             return redirect('login')
#             if 'profile_pic' in request.FILES:
#                 print('found it')
#                 profile.profile_pic = request.FILES['profile_pic']
#             profile.save()
#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = RegisterForm()
#         profile_form = UserProfileInfoForm()
#     return render(request, 'Maggotty/register.html',
#                   {'user_form': user_form,
#                            'profile_form': profile_form,
#                            'registered': registered})

def register(request):
    user_form = RegisterForm(request.POST)
    # profile_form = UserProfileInfoForm(data=request.POST)
    if user_form.is_valid():
        user_form.save()
        username = user_form.cleaned_data.get('username')
        password = user_form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')        
    return render(request, 'Maggotty/register.html',
                  {'user_form': user_form})

def contribute(request):
    # Handle Content Upload
    if request.method == 'POST':
        contribute_title = request.POST['title']
        contribute_img = request.FILES['filename']
        contribute_description = request.POST['comment']

        # create  and save an instance of the Contribute model
        contribution = Contribute(title=contribute_title, upload=contribute_img, description=contribute_description)
        contribution.save()

    return render(request, "Maggotty/contribute.html")


def contributions(request):
    contributions = Contribute.objects.all()[:3]
    return render(request, "Maggotty/contributions.html", {"contributions": contributions})

def polls(request):
    # retrieve all the poll questions from the database
    polls = Poll.objects.all()
    # feedback messages
    message = None

    if request.method == 'POST':
        if '1' in request.POST and '2' in request.POST:
            answer_1 = request.POST['1']
            answer_2 = request.POST['2']
        else:
            answer_1, answer_2 = None, None

        answer_3 = request.POST['opinion']
        if polls:
            question_1 = polls[0].question
            question_2 = polls[1].question
        else:
            question_1, question_2 = None, None
            
        user_poll = UserOpinions(question_1=question_1, question_2=question_2, answers_1=answer_1, answers_2=answer_2, username=request.user, opinion=answer_3)
        user_poll.save()

        message = "Poll created successfully"
    
    return render(request, "Maggotty/polls.html", {"polls": polls, "message": message})

def approvedPolls(request):
    polls = UserOpinions.objects.all() 
    return render(request, "Maggotty/allpolls.html", {"polls": polls})

def alleventslist(request):
    today = date.today().strftime('%Y-%m-%d')
    allEvents = Event.objects.filter(fromDate__range=["2010-01-01", today])
    return render(request, "Maggotty/alleventslist.html", {"allEvents": allEvents})

def upcomingevents(request):
    if request.method == 'POST':
        print(request.POST)
        if request.POST.get('recordID'):
            event_id = int(request.POST.get('recordID'))
            currEvent = Event.objects.filter(id=event_id)[0]
            current_order = Order()
            current_user = request.user
            current_order.username= current_user.username
            current_order.eventID = event_id
            current_order.eventName = currEvent.eventName
            current_order.ticketPrice = currEvent.ticket
            current_order.save()                         
            user_Orders = Order.objects.filter(username=current_user.username, ifPaid=False)
            return render(request, "Maggotty/mycart.html", {"Orders": user_Orders})        
    else:
        today = date.today()
        after_ten_yrs = today.replace(year = today.year + 10)
        today = today.strftime('%Y-%m-%d')
        allEvents = Event.objects.filter(fromDate__range=[today,after_ten_yrs])
        approvedEvents = allEvents.filter(isApproved=True)
        return render(request, "Maggotty/upcomingevents.html", {"allEvents": allEvents, "approvedEvents":approvedEvents})

def createevent(request):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            current_user = request.user
            instance = form.save(commit=False)
            instance.createdBy = current_user.username
            form.save()
            messages.success(request, f'✔️ Event created')
            return redirect('home')
    else:
        form = CreateEventForm()    
    return render(request,'Maggotty/createevent.html',{'form': form})

def contact(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():            
            feedback = form.save()
            messages.success(request, f'✔️ Email has been sent to the Maggotty High Alumni')
            subject = feedback.subject
            message = feedback.comments
            email_from = feedback.email 
            recipient_list = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, email_from, recipient_list) 
            return redirect('home')
    else:
        form = ContactUsForm()    
    return render(request,'Maggotty/contact.html',{'form': form})

def eventdetails(request):
    return render(request, "Maggotty/eventdetails.html")

def newsdetail(request):
    return render(request, "Maggotty/newsdetail.html")

def mycart(request):
    if request.method == 'POST':
            return render(request, "https://paypal.com")      
    current_user = request.user
    user_Orders = Order.objects.filter(username=current_user.username, ifPaid=False)
    return render(request, "Maggotty/mycart.html", {"Orders": user_Orders})

def feedback(request):    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():            
            form.save()
            messages.success(request, f'✔️ Your feedback has been submitted!')            
            return redirect('home')
    else:
        form = FeedbackForm() 
       
    return render(request,'Maggotty/feedback.html',{'form': form})
