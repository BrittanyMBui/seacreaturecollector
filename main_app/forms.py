from django import forms
from .models import Feeding, Creature

class FeedingForm (forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ['date', 'meal', 'feedtime']

class CreatureForm (forms.ModelForm):
    class Meta:
        model = Creature
        fields = ['name', 'species', 'description']