from django.contrib import admin
from .models import Notification, WastePlasticRequestor, LookUp, ContentManagement, RequestPickUp

# Register your models here.
admin.site.register(Notification)
admin.site.register(WastePlasticRequestor)
admin.site.register(LookUp)
admin.site.register(ContentManagement)

class RequestPickUpAdmin(admin.ModelAdmin):
    list_display = ('requestId', 'userId', 'agent_status')
    list_filter = ('agent_status',)
    search_fields = ('requestId__id', 'userId__name', 'agent_status')

admin.site.register(RequestPickUp, RequestPickUpAdmin)

