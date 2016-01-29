from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.template import RequestContext

from .models import User, Category, Image, Item, Notification
from .forms import UserProfileForm, CreateUserForm, AddressForm
from random import shuffle

import json

# Create your views here.

def index(request):
    message = ''
    if request.session['message']:
        message = request.session['message']
    if request.method == 'POST':
        data = request.POST.get('drugs')
        found_entries = Item.objects.get(name = data)
        item_id = found_entries.pk
        return HttpResponseRedirect(reverse("main:results", args = (item_id,)))

    return render(request, 'main/index.html', {'message':message})

def get_drugs(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        drugs = Item.objects.filter(name__icontains = q )[:20]
        data = []
        for drug in drugs:
            drug_json = {}
            drug_json['id'] = drug.pk
            drug_json['label'] = drug.name
            drug_json['value'] = drug.name
            data.append(drug_json)
    else:
        data = 'fail'

    mimetype = 'application/json'
    return JsonResponse(data, safe = False)



def results(request, item_id):
    found_item = get_object_or_404(Item, pk=item_id)
    items = []
    item_category = found_item.category
    if not request.user.is_authenticated():
        items_in_category = item_category.item_set.all()
        for item in items_in_category:
            items.append(item)

    else:
        user_owns = request.user.category_set.all()
        users = item_category.users.all()
        for client in users:
            if client.pk == request.user.pk:
                continue
            client_wants = client.category_set.all()
            #If the client has what the user owns...
            for possession in user_owns:
                for want in client_wants:
                    #Then add all of the items of that client under the category searched for
                    if want.pk == possession.pk:
                        client_has = client.item_set.all()
                        category_id = item_category.pk
                        for item in client_has:
                            if item.category.pk == category_id:
                                items.append(item)

    shuffle(items)
    return render(request, 'main/results.html', {'items':items})

def view_item(request, view_id):
    item = get_object_or_404(Item, pk=view_id)
    logged_in = False
    error = ''
    interested_in = []
    other = []
    if request.user:
        user_items = request.user.item_set.all()
        owner_interests = item.owner.category_set.all()
        for c_item in user_items:
            for interest in owner_interests:
                if c_item.category.pk == interest.pk:
                    interested_in.append(c_item)
                    break
            other.append(c_item)
        logged_in = True
    else:
        user_items = []


    if request.method == 'POST':
        if not request.POST.get("item"):
            error = "You did not select an item to trade for."
        else:
            notification = Notification()
            notification.from_user = request.user
            notification.to_user = item.owner
            notification.to_user_item = item
            notification.from_user_item = Item.objects.get(pk = request.POST.get("item"))
            notification.save()
            return HttpResponseRedirect(reverse('main:confirm', args=(notification.pk,))) #Go to the results page


    return render(request, 'main/view_item.html', {'item':item, 'owner_interests':owner_interests, 'other':other, 'logged_in':logged_in,'error':error})

@login_required
def confirm(request, notification_id):
    notification = get_object_or_404(Notification, pk = notification_id)
    if request.method == 'POST':
        data = request.POST.get('confirm')
        if data == 'yes':
            return HttpResponseRedirect(reverse('main:index'))
        else:
            notification.delete()
            request.session['message'] = "You have cancelled your request of "+notification.to_user_item.name+" in exchange for "+notification.from_user_item.name
            return HttpResponseRedirect(reverse('main:index'))
    return render(request, 'main/confirm.html', {'notification':notification})

@login_required
def respond_to_notification(request, notification_id):
    notification = get_object_or_404(Notification, pk = notification_id)
    notification_history = []
    notification_history.append(notification)
    while not notification.parent_notification is None:
        notification = notification.parent_notification
        notification_history.append(notification)
    client_items = notification.to_user.item_set.all()
    if request.method == 'POST':
        if 'accept' in request.POST:
            return HttpResponseRedirect(reverse('main:make_transaction', args=(notification.pk,)))
        elif 'delete' in request.POST:
            return

    return render(request, 'main/respond_to_notification.html', {'notifications':notification_history, 'client_items':client_items})

@login_required
def confirm_delete(request, notification_id):
    notification = get_object_or_404(Notification, pk = notification_id)
    if request.method == 'POST':
        data = request.POST.get('confirm')
        if data == 'yes':
            return HttpResponseRedirect(reverse('main:index'))
        else:
            notification.delete()
            request.session['message'] = "You have cancelled your request of "+notification.to_user_item.name+" in exchange for "+notification.from_user_item.name
            return HttpResponseRedirect(reverse('main:index'))
    return render(request, 'main/confirm_delete.html', {'notification':notification})


def create_user(request):
    if request.method == 'POST':
        user_form = CreateUserForm(request.POST)
        address_form = AddressForm(request.POST)
        if user_form.is_valid() and address_form.is_valid():
            return #create User
    else:
        user_form = CreateUserForm()
        address_form = AddressForm()

    return render(request, 'main/create_user.html', {'user_form':user_form,'address_form':address_form})


@login_required
def user_profile(request):
    user_notifications = request.user.notification_set.all()
    user = request.user
    address = user.address
    notifications = []
    for notification in user_notifications:
        notification_history = []
        notification_history.append(notification)
        while not notification.parent_notification is None:
            notification = notification.parent_notification
            notification_history.append(notification)
        notifications.append(notification_history)

    user_form = UserProfileForm(instance = user)
    address_form = AddressForm(instance = address)

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instnace = user)
        address_form = AddressForm(request.POST, instance = address)
        if user_form.is_valid() and address_form.is_valid():
            user_form.save()
            address_form.save()

    return render(request, 'main/user_profile.html', {'username':username, 'reputation':reputation, 'user_form':user_form, 'address_form':address_form, 'notifications':notifications, 'user':user})

def view_other_profile(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    items = user.item_set.all()
    return render(request, 'main/view_other_profile', {'first_name':first_name, 'last_name':last_name, 'items':items, 'username':username, 'user':user})

@login_required
def make_transaction(request, notification_id):
    #exchange contact info, etc
    return
