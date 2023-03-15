from django.contrib import admin
from .models import User, Training, Meal, Cardio, Measurement

# Register your models here.
admin.site.register(User)
admin.site.register(Training)
admin.site.register(Meal)
admin.site.register(Cardio)
admin.site.register(Measurement)