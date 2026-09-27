from channels.generic.websocket import AsyncJsonWebsocketConsumer


class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        user = self.scope.get("user")

        if not user or not user.is_authenticated:
            await self.close()
            return

        if user.role != "admin":
            await self.close()
            return

        self.group_name = "admins_notifications"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def notification_message(self, event):

        await self.send_json({
            "id": event["id"],
            "notification_type": event["notification_type"],
            "title": event["title"],
            "message": event["message"],
            "note": event.get("note"),
            "incident": event.get("incident"),
            "created_at": event["created_at"],
        })