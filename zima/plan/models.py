from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    patronymic = models.CharField(max_length=50, blank=True)
    position_in = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=100, blank=True)
    access_level = models.CharField(max_length=20, choices=(
        ('admin', 'Администратор'),
        ('user', 'Пользователь'),
    ), default='user')
    groups = models.ManyToManyField(Group, related_name='custom_user_set')  # Изменено related_name
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')  # Изменено related_name

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Employee(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    position_in = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    # adress_ip = models.CharField(max_length=17)
