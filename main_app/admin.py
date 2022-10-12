from django.contrib import admin

# Register your models here.
from .models import Dog
from .models import Activity
from .models import DogPhoto
from .models import ActivityPhoto
from .models import UserProfile
from .models import TimePunch

admin.site.register(ActivityPhoto)
admin.site.register(Dog)
admin.site.register(Activity)
admin.site.register(DogPhoto)
admin.site.register(UserProfile)
admin.site.register(TimePunch)

