from django.contrib import admin
from .models import Psychologist, Client, Meet, Schedule, Tariff

admin.site.register(Psychologist)
admin.site.register(Client)
admin.site.register(Meet)
admin.site.register(Schedule)
admin.site.register(Tariff)
# Register your models here.
