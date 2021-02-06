from django.shortcuts import render, redirect
from django.http import HttpResponse
import uuid
import boto3
from .models import Creature, Photo
from .forms import FeedingForm, CreatureForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'seacreaturecollector'

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