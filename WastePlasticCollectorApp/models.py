from django.db import models
from geopy.distance import geodesic
from django.db.models.functions import Cast
from django.db.models import FloatField
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
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

TASK_STATUS = [
    ('on progress', 'On Progress'),
    ('completed', 'Completed'),
]


# Create your models here.
class WastePlasticType(models.Model):
    type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.type


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
    wastePlastic_type = models.ForeignKey(WastePlasticType,on_delete=models.CASCADE, null=True, blank=True)
    request_date = models.DateField(default=timezone.now)
    request_time = models.TimeField(default=timezone.now)
    wastePlastic_size = models.PositiveIntegerField()
    wastePlastic_address = models.CharField(max_length=100, null=True, blank=True)
    unique_location = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(max_length=50, null=True, blank=True)
    longitude = models.FloatField(max_length=50, null=True, blank=True)
    waste_plastic_photo = models.ImageField(upload_to='wastPlastic_photos/', null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    pickUp_status=models.CharField(max_length=100, choices=PICK_UP_STATUS, default='pending')

    def __str__(self):
        return self.wastePlastic_address
    @property
    def get_id(self):
        return self.id
    @property
    def get_name(self):
        return self.wastePlastic_address

class RequestPickUp(models.Model):
    requestId = models.ForeignKey(WastePlasticRequestor, on_delete=models.CASCADE)
    userId = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    agent_status = models.CharField(max_length=100, choices=AGENT_STATUS, default='pending')
    
    def __str__(self):
        return f"Request {self.requestId.id} by {self.userId.name} - Status: {self.agent_status}"


class TaskAssigned(models.Model):
    requestId = models.ForeignKey(WastePlasticRequestor, on_delete=models.CASCADE)
    userId = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    assigned_date = models.DateField(default=timezone.now)
    assigned_time = models.TimeField(default=timezone.now)
    asign_status = models.CharField(max_length=100, choices=ASSIGN_STATUS, default='asign')
    task_status = models.CharField(max_length=50, choices=TASK_STATUS, default='on progress')


class Notification(models.Model):
    requestId = models.ForeignKey(WastePlasticRequestor, on_delete=models.CASCADE)
    userId = models.ForeignKey(CustomUsers, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=100, null=True, blank=True)
    message = models.CharField(max_length=100)
    
    def __str__(self):
        return self.message

class LookUp(models.Model):
    unit_price = models.FloatField(default=1.0)
    CO2_reducedValue = models.FloatField(default=1.0)
    
    def __str__(self):
        return f"Unit Price: {self.unit_price}, CO2 Reduced Value: {self.CO2_reducedValue}"


class FeedBack(models.Model):
    user_id = models.ForeignKey(CustomUsers, on_delete=models.CASCADE)
    average_rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], help_text="Rating should be between 1 and 5", blank= True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

class ContentManagement(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
