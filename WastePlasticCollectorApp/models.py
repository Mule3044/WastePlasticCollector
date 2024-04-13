from django.db import models
from UserManagement.models import CustomUsers

# Create your models here.
class WastePlastic(models.Model):
    user = models.ForeignKey(CustomUsers,on_delete=models.CASCADE)
    wastePlastic_type = models.CharField(max_length=100)
    collection_date = models.DateField(auto_now_add=True)
    wastePlastic_size = models.PositiveIntegerField()
    status=models.BooleanField(default=False)

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
    wastePlastic_size = models.PositiveIntegerField()
    wastePlastic_address = models.CharField(max_length=100)
    unique_location = models.CharField(max_length=100)
    latitude = models.FloatField(max_length=50)
    longitude = models.FloatField(max_length=50)

    def __str__(self):
        return self.wastePlastic_type
    @property
    def get_id(self):
        return self.id
    @property
    def get_name(self):
        return self.wastePlastic_type+" "+self.wastePlastic_size