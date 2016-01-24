from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.template import RequestContext

from .search import get_query
from .models import User, Category, Image, Item, SearchField, Notification
from .forms import UserProfileForm, CreateUserForm
from random import shuffle

# Create your views here.


def index(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['text',])
        found_entries = SearchField.objects.filter(entry_query)
        request.session['found_entries'] = found_entries
        request.session['entry_query'] = entry_query
        ]
        return HttpResponseRedirect(reverse('store:results')) #Go to the results page

    return render_to_response('main/index.html',
                          {},
                          context_instance=RequestContext(request))

def results(request):
    if not request.user.is_authenticated():
        found_entries = request.session['found_entries']
        search_fields = SearchField.objects.all()
        items = []
        for field in search_fields: #Going through all search fields
            for entry in found_entries:
                if entry == field: #If a search field match is found
                    items_category = entry.category.item_set.all()
                    for item in items_category:
                        items.append(item)

        items.shuffle()
        return render(request, 'main/results.html', {'items':items})

    else:
        found_entries = request.session['found_entries']
        user_owns = request.user.category_set.all()
        search_fields = SearchField.objects.all()
        items = []
        for field in search_fields: #Going through all search fields
            for entry in found_entries:
                if entry == field.text: #If a search field match is found
                    category = entry.category
                    users = category.users.all()
                    for client in users: #Go through all users who own something in category corresponding to that search field
                        client_wants = client.category_set.all()
                        #If the client has what the user owns...
                        for possession in user_owns:
                            for want in client_wants:
                                #Then add all of the items of that client under the category searched for
                                if want.pk == possession.pk:
                                    client_has = client.item_set.all()
                                    category_id = category.pk
                                    for item in client_has:
                                        if item.category.pk == category_id:
                                            items.append(item)

        items.shuffle()
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

def confirm(request, notification_id):
    notification = get_object_or_404(Notification, pk = notification_id)
    #if user wants to undo, delete notificatoin
    return render(request, 'main/confirm.html', {'notification':notification})

def view_notifications(request):
    #View a user's notfications
    return

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
