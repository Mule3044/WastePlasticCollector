from django.contrib import admin
from .models import Notification, WastePlasticRequestor, LookUp

# Register your models here.
admin.site.register(Notification)
admin.site.register(WastePlasticRequestor)
admin.site.register(LookUp)
