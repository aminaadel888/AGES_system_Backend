from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model

from .models import Notification


User = get_user_model()


def create_admin_notification(
    notification_type,
    title,
    message,
    note=None,
    incident=None
):
    admins = User.objects.filter(
        role="admin"
    )

    channel_layer = get_channel_layer()

    for admin in admins:

        notification = Notification.objects.create(
            recipient=admin,
            notification_type=notification_type,
            title=title,
            message=message,
            note=note,
            incident=incident,
        )

        async_to_sync(
            channel_layer.group_send
        )(
            "admins_notifications",
            {
                "type": "notification_message",

                "id": notification.id,

                "notification_type":
                    notification.notification_type,

                "title":
                    notification.title,

                "message":
                    notification.message,

                "note":
                    notification.note_id,

                "incident":
                    notification.incident_id,

                "created_at":
                    notification.created_at.isoformat(),
            }
        )