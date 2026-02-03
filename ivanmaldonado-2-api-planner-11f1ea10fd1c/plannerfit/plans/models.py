from django.db import models

from users.models import Trainer

class Plan(models.Model) :
    name = models.CharField(max_length=50)
    steps = models.TextField(null = True, blank = True)
    steps_count = models.IntegerField(default = 0)
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    observations = models.TextField(null = True, blank = True)

    def __str__(self) :
        return str(self.name)