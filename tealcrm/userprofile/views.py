from django.shortcuts import render,redirect
# from django.contrib.auth.forms import UserCreationForm (Built in django user creation form )
from .models import Userprofile
from django.contrib.auth.decorators import login_required
from team.models import Team
from userprofile.forms import SignupForm
# Create your views here.

def signup(request):
    if request.method=='POST':
        form= SignupForm(request.POST)


        if form.is_valid():
            user= form.save()

            team=Team.objects.create(name='The Team Name',created_by=user)
            team.members.add(user) 
            team.save()



            Userprofile.objects.create(user=user,active_team = team)



            return redirect('/login/')

    else:
        form =SignupForm()

    return render(request,'userprofile/signup.html',{'form':form})


@login_required
def myaccount(request):
    return render(request,'userprofile/myaccount.html')









