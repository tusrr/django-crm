from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Client
from django.contrib import messages
from .forms import AddClientForm
from team.models import Team
# Create your views here.
@login_required
def clients_list(request):
    clients= Client.objects.filter(created_by=request.user)
    return render(request,'clients/clients_list.html',{'clients':clients})


@login_required
def clients_detail(request,pk):
    client = get_object_or_404(Client, created_by = request.user,pk=pk)
    # client = Client.objects.filter(created_by = request.user).get(pk=pk)

    return render(request,'clients/clients_detail.html',{'client':client})


@login_required
def clients_edit(request,pk):
    client = get_object_or_404(Client, created_by = request.user,pk=pk)
    if request.method =='POST':
        form = AddClientForm(request.POST,instance=client)

        if form.is_valid():
            client.save()

            messages.success(request,'Changes Saved')

            return redirect('clients_list')
    else:
        form= AddClientForm(instance=client)

    return render(request, 'clients/clients_edit.html',{'form':form})




@login_required
def add_client(request):
    team= Team.objects.filter(created_by=request.user)[0]

    if request.method =='POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            team= Team.objects.filter(created_by=request.user).first()
            client = form.save(commit = False)
            client.created_by = request.user
            client.team = team
            client.save()

            messages.success(request,'New Client was created')

            return redirect('clients_list')
    else:
        form= AddClientForm()
    return render(request, 'clients/add_client.html',{'form':form,'team':team})

@login_required
def client_delete(request,pk):
    client = get_object_or_404(Client, created_by = request.user,pk=pk)
    client.delete()

    messages.success(request,'Client was deleted')
    return redirect('clients_list')
