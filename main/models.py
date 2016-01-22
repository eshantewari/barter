from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, UserManager

class Account(User):
    objects = UserManager()
    account_id = models.IntegerField(default = 0)
    address = models.CharField(max_length = 1000)
    reputation = models.IntegerField(default = 0)
    def __unicode__(self):
        return self.username
    

class Category(models.Model):
    name = models.CharField(max_length = 400)
    description = models.TextField()
    users = models.ManyToManyField(Account)
    class Meta:
        verbose_name_plural = "Categories"


class Item(models.Model):
    name = models.CharField(max_length = 400)
    description = models.TextField()
    owner = models.ForeignKey(Account)
    category = models.ForeignKey(Category)
    def __unicode__(self):
        return self.name
    
class Image(models.Model):
    img = models.ImageField(upload_to='item_images', blank=True, null=True)
    item = models.ForeignKey(Item)
    
class SearchField(models.Model):
    text = models.CharField(max_length = 100)
    category = models.ForeignKey(Category)
    
    


    
