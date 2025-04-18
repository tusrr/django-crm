import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import render,redirect, get_object_or_404
# from .forms import AddLeadForm
from .forms import AddCommentForm,AddFileForm
from .models import Lead
from client.models import Client,Comments as ClientComment
from team.models import Team
from django.views import View
from django.views.generic import ListView,DetailView,DeleteView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy



def leads_export(request):
    leads= Lead.objects.filter(created_by=request.user)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="leads_data.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["Name", "Description", "Status", "Priority", "Converted to client", "created at"])
    for lead in leads:
        writer.writerow([lead.name,lead.description,lead.status,lead.priority,lead.converted_to_client,lead.created_at])
    return response

# @login_required
# def leads_list(request):
#     leads=Lead.objects.filter(created_by=request.user)


#     return render(request,'leads/leads_list.html',{'leads':leads})

class LeadListView(LoginRequiredMixin,ListView):
    model = Lead
    template_name = 'leads/leads_list.html'
    context_object_name = 'leads'

    
    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return Lead.objects.filter(created_by=self.request.user,converted_to_client=False)


# @login_required
# def leads_detail(request,pk):
#     lead = get_object_or_404(Lead, created_by = request.user,pk=pk)
#     # lead = Lead.objects.filter(created_by = request.user).get(pk=pk)

#     return render(request,'leads/leads_detail.html',{'lead':lead})

class LeadDetailView(LoginRequiredMixin,DetailView):
    model = Lead
    template_name = "leads/leads_detail.html"

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AddCommentForm()
        context["fileform"] = AddFileForm()

        return context

    


    # def get_object(self):
    #     pk = self.kwargs.get('pk')
    #     return get_object_or_404(Lead,created_by=self.request.user,pk=pk)




    def get_queryset(self):
        return Lead.objects.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))


# @login_required
# def leads_delete(request,pk):
#     lead = get_object_or_404(Lead, created_by = request.user,pk=pk)
#     lead.delete()

#     messages.success(request,'The lead was deleted')

#     return redirect('leads:list')

class LeadDeleteView(LoginRequiredMixin,DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    # def get_queryset(self):
    #      queryset = super(LeadDeleteView, self).get_queryset()

    #      return queryset.filter(created_by=self.request.user,pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
        
        

class LeadUpdateView(LoginRequiredMixin,UpdateView): 
    # specify the model you want to use 
    model = Lead 
    fields = ('name','email','description','priority','status')
  
    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Lead"	
        return context

    def get_queryset(self):
         queryset = super(LeadUpdateView, self).get_queryset()

         return queryset.filter(created_by=self.request.user,pk=self.kwargs.get('pk'))

    success_url = reverse_lazy("leads:list")


# @login_required
# def leads_edit(request,pk):
#     lead = get_object_or_404(Lead, created_by = request.user,pk=pk)
#     if request.method =='POST':
#         form = AddLeadForm(request.POST,instance=lead)

#         if form.is_valid():
#             lead.save()

#             messages.success(request,'Changes Saved')

#             return redirect('leads:list')
#     else:
#         form= AddLeadForm(instance=lead)

#     return render(request, 'leads/leads_edit.html',{'form':form})


class LeadCreateView(LoginRequiredMixin,CreateView):
    model = Lead
    fields = ('name','email','description','priority','status')
    # template_name='leads/add_lead.html'	

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    success_url = reverse_lazy("leads:list")


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team= self.request.user.userprofile.active_team
        context["team"] = team
        context["title"] = "Add Lead"	
        return context
    



    def  form_valid(self, form):
        # team = Team.objects.filter(created_by=self.request.user)[0]

        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team=self.request.user.userprofile.active_team
        self.object.save()
        return redirect(self.get_success_url())

class AddFileView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        pk=kwargs.get('pk')

        form = AddFileForm(request.POST,request.FILES)
        if form.is_valid():
            # team = Team.objects.filter(created_by=self.request.user)[0]
            # team = request.user.userprofile.active_team
            file= form.save(commit=False)
            file.team=self.request.user.userprofile.active_team
            file.lead_id=pk
            file.created_by=request.user
            file.save()

        return redirect('leads:detail',pk=pk)









class AddCommentView(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        pk=kwargs.get('pk')
        # content = request.POST.get('content')

        # print(content)
        # print(pk)

        form = AddCommentForm(request.POST)
        if form.is_valid():
            # team = Team.objects.filter(created_by=self.request.user)[0]
            comment= form.save(commit=False)
            comment.team= self.request.user.userprofile.active_team
            comment.created_by= request.user
            comment.lead_id=pk
            comment.save()

        return redirect('leads:detail',pk=pk)


    




# @login_required
# def add_lead(request):
#     team= Team.objects.filter(created_by=request.user)[0]

#     if request.method =='POST':
#         form = AddLeadForm(request.POST)

#         if form.is_valid():
#             team= Team.objects.filter(created_by=request.user)[0]
#             lead = form.save(commit = False)
#             lead.created_by = request.user
#             lead.team=team
#             lead.save()

#             messages.success(request,'New lead was created')

#             return redirect('leads:list')
#     else:
#         form= AddLeadForm()
#     return render(request, 'leads/add_lead.html',{'form':form,'team':team})


class ConvertToClientView(LoginRequiredMixin,View):
    def get(self,request,pk):
        lead =get_object_or_404(Lead,created_by=request.user,pk=pk)
        team = self.request.user.userprofile.active_team

        client=Client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=request.user, 
            team=team
        )

        lead.converted_to_client=True
        lead.save()


# converting lead comment to client comment

        comments = lead.comments.all()

        for comment in comments:
           ClientComment.objects.create(
                client=client,
                content= comment.content,
                created_by=comment.created_by,
                team=team
           )

        messages.success(request,'The Lead was converted to Client')

        return redirect('leads:list')


# @login_required
# def convert_to_client(request,pk):

#     lead =get_object_or_404(Lead,created_by=request.user,pk=pk)
#     team= Team.objects.filter(created_by=request.user)[0]

#     client=Client.objects.create(
#         name=lead.name,
#         email=lead.email,
#         description=lead.description,
#         created_by=request.user, 
#         team=team
#     )

#     lead.converted_to_client=True
#     lead.save()

#     messages.success(request,'The Lead was converted to Client')

#     return redirect('leads:list')













