from django.db import models
from django.contrib.auth.models import User
class Team(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User,related_name='created_teams' ,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User)
    def __str__(self):
        return self.name