from django.shortcuts import render
from django.http import HttpResponse
from .models import Creature

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
    return render(request, 'creatures/creatures_detail.html', { 'creature': creature })