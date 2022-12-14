
from audioop import add
from distutils.log import Log
from gettext import find
from django.shortcuts import render, redirect
from .models import Dog, DogPhoto, ActivityPhoto, Activity, UserProfile
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import ActivityForm, SignUpForm, UserEditForm, UserProfileForm
from django.urls import reverse_lazy
import geocoder
import folium
from random import randint

import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'sei426-dog-walker-bucket-photo'

### MAP FUNCTION FOR DOG DETAIL ###
def smallmap(dog_id):
    dog = Dog.objects.get(id=dog_id)
    address = dog.owneraddress
    findaddress = geocoder.osm(address)
    lat1 = findaddress.y
    lng1 = findaddress.x
    m = folium.Map(location=[lat1, lng1], zoom_start=16)
    ##Location
    folium.Marker([lat1,lng1], tooltip=f'{dog.name}', popup=f'{dog.owneraddress}').add_to(m)
    m = m._repr_html_()
    context = {
        'm': m,
    }
    return context

# Create your views here.

def about(request):
    return render(request, 'about.html')

def landing(request):
    if request.user.is_authenticated: 
        return render(request, 'home.html')
    else: 
        return render(request, 'landing.html')

@login_required
def home(request):
    dogs_array = Dog.objects.filter(user=request.user)
    count = len(dogs_array)
    activity = 0

    for dog in dogs_array:
        activities = Activity.objects.filter(dog=dog.id)
        activity += len(activities)

    # activity = len(Activity.objects.filter())
    if count > 0:
        count_second = Dog.objects.count()
        random = Dog.objects.all()[randint(0, count_second - 1)]
    else: 
        random = {
            'name': 'No Dog'
        }
    return render(request, 'home.html', {'count': count, 'activity': activity, 'random': random, 'name': profile})

@login_required
def dogs_index(request):
    ## Change this to .filter(userid) when needed
    dogs = Dog.objects.filter(user=request.user)
    return render(request, 'dogs/index.html', {'dogs': dogs})

@login_required
def dogs_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    activity_form = ActivityForm()
    minimap = smallmap(dog_id)
    return render(request, 'dogs/detail.html', {'dog': dog, 'activity_form': activity_form, 'minimap': minimap})

@login_required
def profile(request):
    try: 
        profile = UserProfile.objects.get(user=request.user)
        return render(request, 'users/profile.html', { 'profile': profile})
    except UserProfile.DoesNotExist:
        return render(request, 'users/profile.html')

@login_required
def add_activity(request, dog_id):
    form = ActivityForm(request.POST)
    if form.is_valid():
        new_activity = form.save(commit=False)
        new_activity.dog_id = dog_id
        new_activity.save()
    return redirect('dog_detail', dog_id=dog_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if signup_form.is_valid() and profile_form.is_valid():
            user = signup_form.save()
            new_profile = profile_form.save(commit=False)
            new_profile.user = user
            new_profile.save()
            login(request, user)
            return redirect('home')
        else: 
            error_message = 'Invalid sign up - try again'
    signup_form = UserCreationForm()
    profile_form = UserProfileForm()
    context = {'signup_form': signup_form, 'profile_form': profile_form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# Meant for a general photo upload. May need to configure settings for 'main' profile picture

def add_dog_photo(request, dog_id):
    photo_file = request.FILES.get('photo_file')
    if photo_file:
        s3 = boto3.client('s3')
        ## key = name mod for file. 
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            photo = DogPhoto(url=url, dog_id=dog_id)
            photo.save()
        except Exception as error:
            print(f'error @ upload: {error}')
    return redirect('dog_detail', dog_id=dog_id)

def add_activity_photo(request, activity_id, dog_id):
    activity_photo = request.FILES.get('activity-photo')
    if activity_photo:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:12] + activity_photo.name[activity_photo.name.rfind('.'):]
        try:
            s3.upload_fileobj(activity_photo, BUCKET, key)
            url = f'{S3_BASE_URL}{BUCKET}/{key}'
            photo = ActivityPhoto(url=url, activity_id=activity_id)
            photo.save()
        except Exception as error:
            print(f'Error occured while uploading')
    return redirect('dog_detail', dog_id=dog_id)

def view_photo_profile(request, dogphoto_id):
    photo = DogPhoto.objects.get(id=dogphoto_id)
    return render(request, 'viewimage/profile.html', { 'photo': photo })

def view_photo_activity(request, photo_id):
    photo = ActivityPhoto.objects.get(id=photo_id)
    return render(request, 'viewimage/activity.html', {'photo': photo })

@login_required
def map(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    address = dog.owneraddress
    findaddress = geocoder.osm(address)
    lat1 = findaddress.y
    lng1 = findaddress.x
    m = folium.Map(location=[lat1, lng1], zoom_start=20)
    ##Location
    folium.Marker([lat1,lng1], tooltip=f'{dog.name}', popup=f'{dog.owneraddress}').add_to(m)
    m = m._repr_html_()
    context = {
        'm': m,
    }
    return render(request, 'map/map.html', context )

class DogCreate(LoginRequiredMixin, CreateView):
    model = Dog
    fields = ('name', 'breed', 'coatcolor', 'notes', 'ownername', 'ownerphone', 'owneraddress')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DogUpdate(LoginRequiredMixin, UpdateView):
    model = Dog
    fields = '__all__'

class DogDelete(LoginRequiredMixin, DeleteView):
    model = Dog
    success_url = '/dogs/'

class ActivityDelete(LoginRequiredMixin, DeleteView):
    model = Activity
    success_url = '/dogs/'

class UserEditView(LoginRequiredMixin, UpdateView):
    form_class = UserEditForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('user-profile')

    def get_object(self):
        try:
            profile = UserProfile.objects.get(user=self.request.user)
            return profile
        except:
            return None
