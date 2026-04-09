from django.db import models
from django.utils.translation import gettext_lazy as _

class Room(models.Model):
    name = models.CharField(_("name"), max_length=255, unique=True)

    class Meta:
        verbose_name = _("room")
        verbose_name_plural = _("rooms")

    def __str__(self):
        return self.name

# (ex02)
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages', verbose_name=_("room"))
    sender = models.CharField(_("sender"), max_length=255)
    content = models.TextField(_("content"))
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")

    def __str__(self):
        return f"{self.sender} in {self.room.name} at {self.timestamp}"
