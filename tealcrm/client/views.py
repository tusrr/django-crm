
import csv
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Client
from django.contrib import messages
from .forms import AddClientForm, AddCommentForm,AddFileForm
from team.models import Team
# Create your views here.

@login_required
def clients_export(request):
    clients= Client.objects.filter(created_by=request.user)


    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="clients .csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["Client", "Description", "Created at", "Created by"])

    for client in clients:
        writer.writerow([client.name,client.description,client.created_at,client.created_by])

    return response






@login_required
def clients_list(request):
    clients= Client.objects.filter(created_by=request.user)
    return render(request,'clients/clients_list.html',{'clients':clients})


# @login_required
# def clients_detail(request,pk):
#     client = get_object_or_404(Client, created_by = request.user,pk=pk)
    # client = Client.objects.filter(created_by = request.user).get(pk=pk) -- keep commented 
    # team=Team.objects.filter(created_by=request.user)[0]



    # if request.method=='POST':
    #     form = AddCommentForm(request.POST)
    #     fileform = AddFileForm(request.POST,request.FILES)

    #     if form.is_valid() and fileform.is_valid():
    #         comment= form.save(commit=False)
    #         file= fileform.save(commit=False)
    #         comment.team= team
    #         file.team=team
    #         comment.created_by= request.user
    #         file.created_by= request.user
    #         comment.client=client
    #         file.client=client
    #         comment.save()
    #         file.save()

    #         return redirect('clients:detail',pk=pk)
    
    # else:
    #     form= AddCommentForm()
    #     fileform=AddFileForm()

    
    # return render(request,'clients/clients_detail.html',{'client':client,'form':form,'fileform':fileform})




@login_required
def clients_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    

    if request.method == 'POST':
        # Check which form was submitted by identifying the button clicked
        if 'submit_comment' in request.POST:
            form = AddCommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.team = request.user.userprofile.active_team
                comment.created_by = request.user
                comment.client = client
                comment.save()
                return redirect('clients:detail', pk=pk)
            fileform = AddFileForm()  # Reinitialize file form to avoid errors
        elif 'submit_file' in request.POST:
            fileform = AddFileForm(request.POST, request.FILES)
            if fileform.is_valid():
                file = fileform.save(commit=False)
                file.team = request.user.userprofile.active_team
                file.created_by = request.user
                file.client = client
                file.save()
                return redirect('clients:detail', pk=pk)
            form = AddCommentForm()  # Reinitialize comment form to avoid errors
    else:
        form = AddCommentForm()
        fileform = AddFileForm()

    return render(request, 'clients/clients_detail.html', {'client': client, 'form': form, 'fileform': fileform})



# class AddFileView(View):
#     def post(self,request,*args,**kwargs):
#         pk=kwargs.get('pk')

#         form = AddFileForm(request.POST,request.FILES)
#         if form.is_valid():
#             team = Team.objects.filter(created_by=self.request.user)[0]
#             file= form.save(commit=False)
#             file.team=team
#             file.client_id=pk
#             file.created_by=request.user
#             file.save()

#         return redirect('clients:detail',pk=pk)













@login_required
def clients_edit(request,pk):
    client = get_object_or_404(Client, created_by = request.user,pk=pk)
    if request.method =='POST':
        form = AddClientForm(request.POST,instance=client)

        if form.is_valid():
            client.save()

            messages.success(request,'Changes Saved')

            return redirect('clients:list')
    else:
        form= AddClientForm(instance=client)

    return render(request, 'clients/clients_edit.html',{'form':form})




@login_required
def clients_add(request):
    user_profile = getattr(request.user, 'userprofile', None)
    active_team = user_profile.active_team if user_profile and user_profile.active_team else Team.objects.filter(created_by=request.user).first()
    if request.method =='POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            # team = self.request.user.userprofile.active_team
            client = form.save(commit = False)
            client.created_by = request.user
            client.team = active_team
            client.save()

            messages.success(request,'New Client was created')
            return redirect('clients:list')
    else:
        form= AddClientForm()
    return render(request, 'clients/client_add.html',{'form':form,'active_team':active_team})

@login_required
def client_delete(request,pk):
    client = get_object_or_404(Client, created_by = request.user,pk=pk)
    client.delete()

    messages.success(request,'Client was deleted')
    return redirect('clients:list')
