from django.contrib import admin
from .models import Creature, Feeding, Photo
# Register your models here.
admin.site.register(Creature)
admin.site.register(Feeding)
admin.site.register(Photo)