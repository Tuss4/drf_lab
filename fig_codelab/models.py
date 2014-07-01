from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Foo(models.Model):
    """Test class for migrations in code lab 3"""
    name = models.CharField(max_length=100)
    is_bar = models.NullBooleanField(default=False)
    age = models.CharField(max_length=2, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Employee(models.Model):
    """
    Django Rest Framework code lab
    Employee model
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=7, decimal_places=2)
    start_date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    class Meta:
        ordering = ['last_name']
