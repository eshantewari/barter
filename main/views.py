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

from .models import User, Category, Image, Item, SearchField, Notification
from .forms import UserProfileForm, CreateUserForm
from random import shuffle

import json

# Create your views here.

def index(request):
    if request.method == 'POST':
        data = request.POST.get('drugs')
        found_entries = Item.objects.get(name = data)
        item_id = found_entries.pk
        return HttpResponseRedirect(reverse("main:results", args = (item_id,)))

    return render(request, 'main/index.html')

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

    if request.method == 'POST':
        notification = Notification()
        notification.from_user = request.user
        notification.to_user = item.owner
        notification.item = item
        notification.save()

        return HttpResponseRedirect(reverse('main:confirm', args=(notification.pk,))) #Go to the results page

    return render(request, 'main/view_item.html', {'item':item})

@login_required
def confirm(request, notification_id):
    notification = get_object_or_404(Notification, pk = notification_id)
    #if user wants to undo, delete notificatoin
    return render(request, 'main/confirm.html', {'notification':notification})

@login_required
def view_notifications(request):
    #View a user's notfications
    return

@login_required
def make_transaction(request):
    #exchange contact info, etc
    return


def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user.save()
    else:
        form = CreateUserForm(instance = user)

    return render(request, 'main/create_user.html', {'form':form})


@login_required
def user_profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('store:create_user')) #Go to the create user page

    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance = user)
        if form.is_valid():
            user.save()
    else:
        form = UserProfileForm(instance = user)

    return render(request, 'main/user_profile.html', {'username':username, 'reputation':reputation, 'form':form})

def view_other_profile(request):
    return
