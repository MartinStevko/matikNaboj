from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Druzinka(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.PROTECT) # , default=1
    name = models.CharField(max_length=100, unique=True)

    points = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)

    me_x = models.IntegerField(blank=False, editable=True, default=10)
    me_y = models.IntegerField(blank=False, editable=True, default=10)

    def __str__(self):
        return "{}".format(self.name)

class Goal(models.Model):
    idDruzinka = models.ForeignKey(Druzinka, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)

    x = models.IntegerField(blank=False, editable=True)
    y = models.IntegerField(blank=False, editable=True)

    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Ciel {} druzinky {}".format(self.id, self.idDruzinka.name)

class Message(models.Model):
    importance = models.BooleanField(default=False)
    text = models.TextField(editable=True)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.importance:
            return "Important message - {}".format(self.id)
        else:
            return "Message {}".format(self.id)
