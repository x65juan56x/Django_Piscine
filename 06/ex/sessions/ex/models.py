from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    @property
    def reputation(self):
        rep = 0
        for tip in self.tips.all():
            rep += tip.upvotes.count() * 5
            rep -= tip.downvotes.count() * 2
        return rep

    def has_perm(self, perm, obj=None):
        if perm == 'ex.can_downvote' and self.reputation >= 15:
            return True
        if perm == 'ex.delete_tip' and self.reputation >= 30:
            return True
        return super().has_perm(perm, obj)

class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tips")
    date = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvoted_tips', blank=True)
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='downvoted_tips', blank=True)

    class Meta:
        permissions = [
            ("can_downvote", "Can downvote a tip"),
        ]

    def __str__(self):
        return f"Tip by {self.author.username} at {self.date.strftime('%Y-%m-%d %H:%M')}"
