from django.db import models
from UserManagement.models import CustomUsers

PICK_UP_STATUS = [
    ('approved', 'Approved'),
    ('pending', 'Pending'),
    ('canceled', 'Canceled'),
    ('completed', 'Completed'),
]
AGENT_STATUS = [
    ('accept', 'Accept'),
    ('reject', 'Reject'),
    ('pending', 'Pending'),

]
REQUEST_HISTORY = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('canceled', 'Canceled'),
]

ASSIGN_STATUS = [
    ('asign', 'Asign'),
    ('take back', 'Take back'),
]

# Create your models here.
class WastePlastic(models.Model):
    user = models.ForeignKey(CustomUsers,on_delete=models.CASCADE)
    wastePlastic_type = models.CharField(max_length=100)
    collection_date = models.DateField(auto_now_add=True)
    wastePlastic_size = models.PositiveIntegerField()
    pickUp_status=models.CharField(max_length=100, choices=PICK_UP_STATUS, default='pending')

    def __str__(self):
        return self.wastePlastic_type
    @property
    def get_id(self):
        return self.id
    @property
    def get_name(self):
        return self.wastePlastic_type+" "+self.wastePlastic_size

class WastePlasticRequestor(models.Model):
    requestor = models.ForeignKey(CustomUsers,on_delete=models.CASCADE)
    wastePlastic_type = models.CharField(max_length=100)
    request_date = models.DateField(auto_now_add=True)
    request_time = models.TimeField(auto_now_add=True)
    wastePlastic_size = models.PositiveIntegerField()
    wastePlastic_address = models.CharField(max_length=100, null=True, blank=True)
    unique_location = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(max_length=50, null=True, blank=True)
    longitude = models.FloatField(max_length=50, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    pickUp_status=models.CharField(max_length=100, choices=PICK_UP_STATUS, default='pending')

    def __str__(self):
        return self.wastePlastic_type
    @property
    def get_id(self):
        return self.id
    @property
    def get_name(self):
        return self.wastePlastic_type+" "+self.wastePlastic_size

class RequestPickUp(models.Model):
    requestId = models.ForeignKey(WastePlasticRequestor, on_delete=models.CASCADE)
    userId = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    agent_status = models.CharField(max_length=100, choices=AGENT_STATUS, default='pending')


class TaskAssigned(models.Model):
    requestId = models.ForeignKey(WastePlasticRequestor, on_delete=models.CASCADE)
    userId = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    asign_status = models.CharField(max_length=100, choices=ASSIGN_STATUS, default='asign')



class Notification(models.Model):
    request_id = models.ForeignKey(WastePlasticRequestor, on_delete=models.CASCADE)
    notification = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.notification

class LookUp(models.Model):
    unit_price = models.FloatField(default=1.0)
    CO2_reducedValue = models.FloatField(default=1.0)
    
    def __str__(self):
        return f"Unit Price: {self.unit_price}, CO2 Reduced Value: {self.CO2_reducedValue}"