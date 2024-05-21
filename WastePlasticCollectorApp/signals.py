from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification, WastePlasticRequestor, WastePlastic, RequestPickUp, TaskAssigned

@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'public_room',
            {
                "type": "send_notification",
                "message": instance.message
            }
        )
@receiver(post_save, sender=WastePlasticRequestor)
def waste_plastic_requestor_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'public_room',
            {
                "type": "send_notification",
                "message": instance.message
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

