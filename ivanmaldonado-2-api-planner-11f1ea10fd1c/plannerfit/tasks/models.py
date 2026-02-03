from django.db import models
from users.models import Trainer

# Objeto de las tareas
class Task(models.Model):
    name = models.CharField(max_length=50)
    display = models.BooleanField(default = 1) # 0 = hidden | 1 = display
    video_url = models.CharField(max_length=100, null = True, blank = True)
    audio = models.FileField(upload_to='audios', null = True, blank = True)
    description = models.CharField(max_length=100, null = True, blank = True)
    user = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self) :
        return str(self.name)

