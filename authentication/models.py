from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models

User._meta.get_field("email")._unique = True


class UsedPasswordResetToken(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=255, db_index=True)
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "token")
