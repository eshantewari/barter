from __future__ import unicode_literals

from django.db import models
import re
from django.db import models
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import User, UserManager

class User(AbstractBaseUser, PermissionsMixin):

	class Meta:
		#app_label = 'accounts'
		db_table = "user"
		#ordering=["created"]

	username = models.CharField(_('username'), max_length=75, unique=True,
	help_text=_('Required. 30 characters or fewer. Letters, numbers and '
	'@/./+/-/_ characters'),
	validators=[
	validators.RegexValidator(re.compile('^[\w.@+-]+$'),
	_('Enter a valid username.'), 'invalid')
	])
	first_name = models.CharField(_('First Name'), max_length=254)
	last_name = models.CharField(_('short name'), max_length=30)
	email = models.EmailField(_('email address'), max_length=254, unique=True)
	is_staff = models.BooleanField(_('staff status'), default=False,
	help_text=_('Designates whether the user can log into this admin '
	'site.'))
	is_active = models.BooleanField(_('active'), default=True,
	help_text=_('Designates whether this user should be treated as '
	'active. Unselect this instead of deleting accounts.'))
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

	objects = UserManager()

	reputation = models.IntegerField(default = 0)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	profile_pic = models.ImageField(upload_to='profile_pics')


	def get_full_name(self):
		return self.full_name

	def get_short_name(self):
		return self.username

	def __unicode__(self):
		return self.username

class Category(models.Model):
    name = models.CharField(max_length = 400)
    description = models.TextField()
    users = models.ManyToManyField(User)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length = 400)
    description = models.TextField()
    owner = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Image(models.Model):
    img = models.ImageField(upload_to='item_images', blank=True, null=True)
    item = models.ForeignKey(Item, blank = True, null = True)

class Address(models.Model):
	user = models.OneToOneField(User)
	street = models.CharField(max_length = 100)
	city = models.CharField(max_length = 100)
	zip_code = models.CharField(max_length = 5)

class Notification(models.Model):
	to_user = models.ForeignKey(User, related_name = "to_user")
	from_user = models.ForeignKey(User, related_name = "from_user")
	to_user_item = models.ForeignKey(Item, related_name = "to_user_item")
	from_user_item = models.ForeignKey(Item)
	parent_notification = models.ForeignKey('self')
