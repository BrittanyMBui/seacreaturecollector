from django.shortcuts import render, redirect
from django.http import HttpResponse
import uuid
import boto3
from .models import Creature, Photo
from .forms import FeedingForm, CreatureForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'seacreaturecollector'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def creatures_index(request):
    if request.method == "POST":
        creature_form = CreatureForm(request.POST)
        if creature_form.is_valid():
            new_creature = creature_form.save(commit=False)
            new_creature.user = request.user
            new_creature.save()
            return redirect('creatures_index')

    creatures = Creature.objects.filter(user=request.user)
    creature_form = CreatureForm()
    context = {
        'creatures': creatures,
        'creature_form': creature_form
    }
    return render(request, 'creatures/creatures_index.html', context)

@login_required
def creatures_detail(request, creature_id):
    creature = Creature.objects.get(id=creature_id)
    feeding_form = FeedingForm()
    context = {
        'creature': creature,
        'feeding_form': feeding_form,
    }
    return render(request, 'creatures/creatures_detail.html', context)

@login_required
def add_feeding(request, creature_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.creature_id = creature_id
        new_feeding.save()
    return redirect('detail', creature_id=creature_id)

@login_required
def add_photo(request, creature_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            photo = Photo(url=url, creature_id=creature_id)
            photo.save()
        except:
            print('An error occured uploading file to S3')
        return redirect('detail', creature_id=creature_id)

# def delete_photo(request, creature_id, photo_id):
#     if request.method == "POST":

#         try:
#             s3 = boto3.client('s3')
#             s3.delete_object(creature_id=creature_id, photo_id=photo_id)
#             return redirect('creatures_detail')

def signup(request):
    error_message = ''
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('creatures_index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {
        'form': form, 'error_message': error_message
    }
    return render(request, 'registration/signup.html', context)

@login_required
def delete_creature(request, creature_id):
    if request.method == "POST":
        creature = Creature.objects.get(id=creature_id)
        creature.delete()
        return redirect('creatures_index')

@login_required
def edit_creature(request, creature_id):
    creature = Creature.objects.get(id=creature_id)

    if request.method == "GET":
        creature_form = CreatureForm(instance=creature)
        context = {
            'form': creature_form
        }
        return render(request, 'creatures/creatures_edit.html', context)
    
    else:
        creature_form = CreatureForm(request.POST, instance=creature)
        if creature_form.is_valid():
            creature_form.save()
            return redirect('detail', creature_id=creature_id)
