from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from math import radians, cos, sin, asin, sqrt
from .models import Notification, WastePlasticRequestor, WastePlastic, RequestPickUp, TaskAssigned
from UserManagement.models import CustomUsers


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

def find_nearest_agent(requestor):
    agents = CustomUsers.objects.filter(role='agent', is_active=True)
    nearest_agent = None
    min_distance = float('inf')

    for agent in agents:
        if agent.latitude is not None and agent.longitude is not None:
            distance = haversine(requestor.longitude, requestor.latitude, agent.longitude, agent.latitude)
            if distance < min_distance:
                min_distance = distance
                nearest_agent = agent

    return nearest_agent, min_distance

@receiver(post_save, sender=WastePlasticRequestor)
def waste_plastic_requestor_created(sender, instance, created, **kwargs):
    if created:
        # Find the nearest agent
        nearest_agent, distance = find_nearest_agent(instance)
        if nearest_agent:
            # Create a RequestPickUp record
            request_pickup = RequestPickUp.objects.create(
                requestId=instance,
                userId=nearest_agent,
                agent_status='pending'
            )

            # Create a TaskAssigned record
            task_assigned = TaskAssigned.objects.create(
                requestId=instance,
                userId=nearest_agent,
                asign_status='asign',
                task_status='on progress',
                assigned_date=timezone.now().date(),
                assigned_time=timezone.now().time()
            )

            # Prepare the notification message
            message = f'A new waste plastic request has been made by {instance.requestor.name}. The distance to the requestor is approximately {distance:.2f} km.'

            # Register the notification in the Notification table
            Notification.objects.create(
                requestId=instance,
                userId=nearest_agent,
                title='New Waste Plastic Request',
                message=message
            )

            # Send notification using Django Channels
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'user_{nearest_agent.id}',
                {
                    "type": "send_notification",
                    "message": message
                }
            )


@receiver(post_save, sender=RequestPickUp)
def create_task_assigned(sender, instance, created, **kwargs):
    # Check if agent_status is 'accept'
    if instance.agent_status == 'accept':
        # Create or update the TaskAssigned entry
        TaskAssigned.objects.update_or_create(
            requestId=instance.requestId,
            userId=instance.userId,
            defaults={'asign_status': 'asign'}
        )
