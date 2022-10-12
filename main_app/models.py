from re import M
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

"""
================
MAIN MODELS
================
"""

class Dog(models.Model):
    ## Dog Description
    name= models.CharField(max_length=20, verbose_name=('Name'))
    breed= models.CharField(max_length=20, verbose_name=('Breed'))
    coatcolor= models.CharField(max_length=15, verbose_name=('Coat Color'))
    notes= models.TextField(max_length=250, verbose_name=('Notes'))
    ## Owner contact
    ownername= models.CharField(max_length=20, verbose_name=('Owner Name'))
    ownerphone= models.CharField(max_length=10, verbose_name=('Owner Phone'))
         ### Should ownerADDRESS be changed to TextField?  ****
    owneraddress= models.CharField(max_length=100, verbose_name=('Owner Address'))
    ## user/walker FK
    user= models.ForeignKey(User, on_delete=models.CASCADE)

    """
    ManyToMany field not defined yet
    """

    def __str__(self):
        return f'{self.name}\'s model. FK @ {self.user}'

    def get_absolute_url(self):
        return reverse('dog_detail', kwargs={'dog_id': self.id})

class Activity(models.Model):
    ##Activity info
    date= models.DateField('activity date')
    activity= models.TextField(max_length=250)
    ## dog FK
    dog= models.ForeignKey(Dog, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date}||{self.dog.name}: {self.activity}'

    ### **** Having issues enabling this?
    class Meta:
        # ordering = ['-date']
        pass

"""
=============
Extended Models
=============
"""


"""
*** Need to implement boto3 and environ.
    Need to generate s3 account for bucket
"""
class DogPhoto(models.Model):
    url = models.CharField(max_length=200)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.dog.name}\'s photo  url: {self.url}'


########### Placeholder, may not use at all
class ActivityPhoto(models.Model):
    url = models.CharField(max_length=200)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, verbose_name=('First Name'))
    last_name = models.CharField(max_length=100, verbose_name=('Last Name'))
    email = models.EmailField(max_length=100, verbose_name=('Email'))
    phone = models.CharField(max_length=10, verbose_name=('Phone Number'))
    address = models.CharField(max_length=100, verbose_name=('Address'))

    def __str__(self):
        return str(self.user)

TIME_PUNCH_CHOICES = (
    ('clock_in', 'Clock In'),
    ('clock_out', 'Clock Out')
)

class TimePunch(models.Model):
    date_time = models.DateTimeField(verbose_name=('Date/Time'))
    punch_type = models.CharField(max_length=20, choices=TIME_PUNCH_CHOICES)

    user= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date_time}: {self.punch_type}'
