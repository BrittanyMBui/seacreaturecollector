from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Creature
from .forms import FeedingForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def creatures_index(request):
    creatures = Creature.objects.all()
    return render(request, 'creatures/creatures_index.html', { 'creatures': creatures })

def creatures_detail(request, creature_id):
    creature = Creature.objects.get(id=creature_id)
    feeding_form = FeedingForm()
    context = {
        'creature': creature,
        'feeding_form': feeding_form,
    }
    return render(request, 'creatures/creatures_detail.html', context)

def add_feeding(request, creature_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.creature_id = creature_id
        new_feeding.save()
    return redirect('detail', creature_id=creature_id)