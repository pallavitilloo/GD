import re
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from Maggotty.forms import UserForm, UserProfileInfoForm, CreateEventForm
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

# class IndexView(ListView):
#     template_name = 'Maggotty/index.html'
#     context_object_name = 'event_list'

#     def get_queryset(self):
#         return Event.objects.all()

# class EventDetailView(DetailView):
#     model = Event
#     template_name = 'Maggotty/eventdetails.html'

# def edit(request, pk, template_name='Maggotty/edit.html'):
#     event = get_object_or_404(Event, pk=pk)
#     # form = CreateEventForm(request.POST or None, instance=post)
#     form = CreateEventForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('home')
#     return render(request, template_name, {'form':form})

# def delete(request, pk, template_name='Maggotty/confirm_delete.html'):
#     event = get_object_or_404(Event, pk=pk)
#     if request.method=='POST':
#         event.delete()
#         return redirect('home')
#     return render(request, template_name, {'object':event})



from Maggotty.models import Contribute, Poll, UserOpinions

def home(request):
    return render(request, "Maggotty/home.html")

def about(request):
    return render(request, "Maggotty/about.html")

def contact(request):
    return render(request, "Maggotty/contact.html")

def donate(request):
    return render(request, "Maggotty/donate.html")

def faq(request):
    return render(request, "Maggotty/faq.html")

def feedback(request):
    return render(request, "Maggotty/feedback.html")

def history(request):
    return render(request, "Maggotty/history.html")

def mission(request):
    return render(request, "Maggotty/mission.html")

def news(request):
    return render(request, "Maggotty/news.html")

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            messages.success(request, f'✔️ User account created successfully for {user}. You can login and access your account now!')
            return redirect('home')
            return redirect('login')
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'Maggotty/register.html',
                  {'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})

def contribute(request):
    """Handle Content Upload"""
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
    
    return render(request, "Maggotty/polls.html", {"polls": polls})

def approvedPolls(request):
    polls = UserOpinions.objects.filter(approved=True)
    return render(request, "Maggotty/allpolls.html", {"polls": polls})


# def event(request):
#     return render(request, "Maggotty/event.html")

def alleventslist(request):
    today = date.today().strftime('%Y-%m-%d')
    allEvents = Event.objects.filter(fromDate__range=["2010-01-01", today])
    return render(request, "Maggotty/alleventslist.html", {"allEvents": allEvents})

def upcomingevents(request):
    if request.method == 'POST':
        if request.POST.get('eventID') and request.POST.get('ticket') and request.POST.get('eventName'):
            current_order = Order()
            current_order.username= request.user.username
            current_order.eventID = request.POST.get('eventID')
            current_order.eventName = request.POST.get('eventName')
            current_order.ticketPrice = request.POST.get('ticket')
            current_order.save()  
            current_user = request.user           
            user_Orders = Order.objects.filter(username=current_user.username)
            return render(request, "Maggotty/mycart.html", {"Orders": user_Orders})
    else:
        today = date.today()
        after_ten_yrs = today.replace(year = today.year + 10)
        today = today.strftime('%Y-%m-%d')
        allEvents = Event.objects.filter(fromDate__range=[today,after_ten_yrs])
        return render(request, "Maggotty/upcomingevents.html", {"allEvents": allEvents})

    

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

def eventdetails(request):
    return render(request, "Maggotty/eventdetails.html")

def newsdetail(request):
    return render(request, "Maggotty/newsdetail.html")

def mycart(request):
    if request.method == 'POST':
            return render(request, "https://paypal.com")      
    current_user = request.user
    user_Orders = Order.objects.filter(username=current_user.username)
    return render(request, "Maggotty/mycart.html", {"Orders": user_Orders})
    