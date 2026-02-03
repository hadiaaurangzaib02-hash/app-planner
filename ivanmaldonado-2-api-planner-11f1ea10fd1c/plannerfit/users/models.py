from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from django.utils import timezone
from plannerfit.settings.common import CODE_LOGIN_EXPIRATION_TIME
from .managers import TrainerManager
import random
import string

class Trainer(AbstractUser):
    username = models.CharField(_('username'), max_length=100, null = True, default = None)
    email = models.CharField(_('email address'), max_length=100, unique=True)
    code = models.CharField(_('Email token'), max_length=10, null = True, default = None)
    code_expiration = models.DateTimeField(null = True, default = None)
    surname = models.CharField(_('Surnames'), max_length=50, null = True, default = None)
    nickname = models.CharField(_('Nickname'), null=True,default = None, max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = TrainerManager()

    def __str__(self):
        return self.email

    def generate_random_code(self) :
        code = ''.join(random.sample(string.ascii_uppercase, 8))
        self.code = code
        self.code_expiration = timezone.now() + timedelta(hours=CODE_LOGIN_EXPIRATION_TIME)
        self.save()
        return code 
        
    def clear_code(self) :
        self.code = None
        self.code_expiration = None 
        self.save()

    def check_code(self, code) :
        if code == self.code:
            if timezone.now() > self.code_expiration :
                return False
            else :
                return True
        return False
    
    def check_integrity_code(self) : 
        if self.code :
            if timezone.now() <= self.code_expiration :
                return True 
        return False
         
    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

# Objeto de las tareas
class Client(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=80)
    phone = models.CharField(max_length=20, null = True, blank = True)
    email = models.EmailField(max_length=40, null = True, blank = True)
    observations = models.TextField(null = True, blank = True)
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True)
    last_login_datetime = models.DateTimeField(null=True, blank=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    status = models.BooleanField(default=True) # true = active, false = inactive
    plans_assigned = models.ManyToManyField("plans.Plan", related_name="plans_assigned", null = True, blank = True)
    plans_completed = models.ManyToManyField("plans.Plan", related_name="plans_completed", null = True, blank = True)
    plans_discarded = models.ManyToManyField("plans.Plan", related_name="plans_discared", null = True, blank = True)
    plans_favorite = models.ManyToManyField("plans.Plan", related_name="plans_favorite", null = True, blank = True)
    last_plan = models.ForeignKey("plans.Plan", related_name="last_plan", on_delete=models.CASCADE, null = True, blank = True)
    link = models.CharField(max_length=30, null = True, blank = True)
    
    def __str__(self) :
        return str(self.name)
