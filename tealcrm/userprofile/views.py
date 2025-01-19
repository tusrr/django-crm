from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Userprofile
from django.contrib.auth.decorators import login_required
from team.models import Team
# Create your views here.

def signup(request):
    if request.method=='POST':
        form= UserCreationForm(request.POST)


        if (form.is_valid()):
            user= form.save()

            team=Team.objects.create(name='The Team Name',created_by=request.user)
            team.members.add(request.user) 
            team.save()



            Userprofile.objects.create(user=user)



            return redirect('/login/')

    else:
        form =UserCreationForm()

    return render(request,'userprofile/signup.html',{'form':form})


@login_required
def myaccount(request):
    team= Team.objects.filter(created_by=request.user)[0]
    return render(request,'userprofile/myaccount.html',{'team':team})









