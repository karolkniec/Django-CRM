from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Agent, Lead
from .forms import LeadModelForm

def lead_list(request):
    leads = Lead.objects.all()
    return render(request, 'leads/lead_list.html', {"leads": leads})

def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }

    return render(request, 'leads/lead_detail.html', context)

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

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')