from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from math import radians, cos, sin, asin, sqrt
from .models import Notification, WastePlasticRequestor, WastePlastic, RequestPickUp, TaskAssigned
from UserManagement.models import CustomUsers


# @receiver(post_save, sender=Notification)
# def notification_created(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'public_room',
#             {
#                 "type": "send_notification",
#                 "message": instance.message
#             }
#         )

# @receiver(post_save, sender=WastePlasticRequestor)
# def waste_plastic_requestor_created(sender, instance, created, **kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'public_room',
#             {
#                 "type": "send_notification",
#                 "message": instance.message
#             }
#         )
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
            RequestPickUp.objects.create(
                requestId=instance,
                userId=nearest_agent,
                agent_status='pending'
            )

            # Prepare the notification message
            message = f'A new waste plastic request has been made by {instance.requestor.name}. The distance to the requestor is approximately {distance:.2f} km.'

            # Send notification using Django Channels
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'public_room',
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

# @receiver(post_save, sender=WastePlasticRequestor)
# def notify_request_pickup(sender, instance, created, **kwargs):
#     if created:
#         # Notify all RequestPickUp objects about the new WastePlasticRequestor
#         message = f"New waste plastic request available: {instance}"
#         for request_pickup in RequestPickUp.objects.filter(agent_status='pending'):
#             Notification.objects.create(
#                 wastePlasticRequest=instance,
#                 message=message
#             )

# @receiver(post_save, sender=RequestPickUp)
# def assign_task_to_nearest_agent(sender, instance, **kwargs):
#     if instance.agent_status == 'accepted':
#         requestor = instance.requestId
#         requestor_coords = (requestor.latitude, requestor.longitude)
        
#         nearest_pickup = None
#         min_distance = float('inf')
        
#         for request_pickup in RequestPickUp.objects.filter(agent_status='accepted'):
#             pickup_coords = (request_pickup.latitude, request_pickup.longitude)
#             distance = geodesic(requestor_coords, pickup_coords).kilometers
            
#             if distance < min_distance:
#                 min_distance = distance
#                 nearest_pickup = request_pickup
        
#         if nearest_pickup:
#             TaskAssigned.objects.create(
#                 requestId=requestor,
#                 userId=nearest_pickup.userId,
#                 asign_status='asign',
#                 task_status='on progress'
#             )