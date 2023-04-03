from django.core.mail import send_mail
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Agent, Lead
from .forms import LeadModelForm, CustomUserCreationForm

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

###################################################

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"

def landing_page(request):
    return render(request, "landing.html")

###################################################

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"

def lead_list(request):
    leads = Lead.objects.all()
    return render(request, 'leads/lead_list.html', {"leads": leads})

####################################################

class LeadDetailView(OrganisorAndLoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"

def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }

    return render(request, 'leads/lead_detail.html', context)

#####################################################

class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        send_mail(
            subject="A lead has been created",
            message="Check the email. New lead has arrived!",
            from_email="test@test.com",
            recipient_list=['test2@test2.com']
        )

        return super(LeadCreateView, self).form_valid(form)

def lead_create(request):
    form = LeadModelForm()

    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            #first_name = form.cleaned_data['first_name']
            #last_name = form.cleaned_data['last_name']
            #age = form.cleaned_data['age']
            #agent = form.cleaned_data['agent']
            #Lead.objects.create(
            #    first_name=first_name,
            #    last_name=last_name,
            #    age=age,
            #    agent=agent
            #)
            print("Lead has been created!")
            return redirect('/leads')

    context = {
        "form": form
    }
    return render(request, 'leads/lead_create.html', context)

#########################################################

class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('/leads')

    form = LeadModelForm(instance=lead)
    context = {
        'form': form,
        'lead': lead
    }

    return render(request, 'leads/lead_update.html', context)

##########################################################

class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self) -> str:
        return reverse("leads:lead-list")

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')