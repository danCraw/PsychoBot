from django.contrib import admin
from .models import Psychologist, Client, Meet, Schedule, Tariff, Specialization

admin.site.register(Psychologist)
admin.site.register(Client)
admin.site.register(Meet)
admin.site.register(Schedule)
admin.site.register(Tariff)
admin.site.register(Specialization)
# Register your models here.
