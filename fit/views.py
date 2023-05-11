from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Training, Meal, Cardio, Measurement
from django.urls import reverse
from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . import helpers
from django.core.paginator import Paginator

# Days and hours for the dropdown lists
days = [("Monday", "Monday"), ("Tuesday", "Tuesday"), ("Wednesday", "Wednesday"), ("Thursday", "Thursday"), ("Friday", "Friday"), 
        ("Saturday", "Satuday"), ("Sunday", "Sunday")]
time = [("00:00-06:00", "00:00-06:00"), ("06:00-08:00", "06:00-08:00"), ("08:00-10:00", "08:00-10:00"), 
        ("10:00-12:00", "10:00-12:00"),("12:00-14:00", "12:00-14:00"), ("14:00-16:00", "14:00-16:00"), ("16:00-18:00", "16:00-18:00"), 
        ("18:00-20:00", "18:00-20:00"), ("20:00-22:00", "20:00-22:00"), ("22:00-00:00", "22:00-00:00")]


class BmiForm(forms.Form):
    height = forms.IntegerField(
        label = "height",
        widget=forms.NumberInput(attrs={'placeholder': 'height (cm)'})
    )
    weight = forms.IntegerField(
        label = "weight",
        widget=forms.NumberInput(attrs={'placeholder': 'weight (kg)'})
    )

class TimerForm(forms.Form):
    work = forms.IntegerField(
        label = "work",
        widget=forms.NumberInput(attrs={'placeholder': 'work (seconds)'})
    )
    rest = forms.IntegerField(
        label = "rest",
        widget=forms.NumberInput(attrs={'placeholder': 'rest (seconds)'})
    )
    interval = forms.IntegerField(
        label = "inteval",
        widget=forms.NumberInput(attrs={'placeholder': 'interval'})
    )

class TrainMealForm(forms.Form):
    Name = forms.CharField(
        label = False,
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Name'})
        )
    Description = forms.CharField(
        label = False,
        max_length = 600, 
        widget=forms.Textarea(attrs={"rows":5, "cols":20, 'placeholder': 'Description' }))
    Day = forms.CharField(
        max_length=10,
        label='Day', widget=forms.Select(choices=days)
        )
    Time = forms.CharField(
        max_length=12,
        label='Time', widget=forms.Select(choices=time)
        )
    
class CardioForm(forms.Form):
    Date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    Distance = forms.FloatField(
        label = "Distance", min_value = 0.1,
        widget=forms.NumberInput(attrs={'placeholder': 'Distance (km)'})
    )
    Time = forms.IntegerField(
        label='Time', min_value = 1,
        widget=forms.NumberInput(attrs={'placeholder': 'Time (minutes)'})
        )
    Discipline = forms.CharField(
        max_length=20,
        label='Discipline', widget=forms.Select(choices=[("Running", "Running"), ("Cycling", "Cycling")])
        )
    
class MeasurementForm(forms.Form):
    Date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    Weight = forms.FloatField(
        label = "Weight", min_value = 0.1,
        widget=forms.NumberInput(attrs={'placeholder': 'Weight (kg)'})
    )
    Waist = forms.FloatField(
        label = "Waist", min_value = 0.1, required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Waist (cm)'})
    )
    Chest = forms.FloatField(
        label = "Chest", min_value = 0.1, required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Chest (cm)'})
    )
    Thigh = forms.FloatField(
        label = "Thigh", min_value = 0.1, required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Thigh (cm)'})
    )
    Arm = forms.FloatField(
        label = "Arm", min_value = 0.1, required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Arm (cm)'})
    )
    Notes = forms.CharField(
        label = False, required=False,
        max_length = 200, 
        widget=forms.Textarea(attrs={"rows":5, "cols":20, 'placeholder': 'Notes' }))


def index(request):
    return render(request, "fit/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "fit/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "fit/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "fit/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "fit/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "fit/register.html")

def bmi(request):
    return render(request, "fit/bmi.html", {
        "bmi": BmiForm()
    })

def interval(request):
    return render(request, "fit/interval.html", {
        "timer": TimerForm()
    })

def training(request):
    if request.method == "POST":
        form = TrainMealForm(request.POST)
        if form.is_valid():
            # Collect values from the form
            name = form.cleaned_data["Name"]
            description = form.cleaned_data["Description"]
            day = form.cleaned_data["Day"]
            time = form.cleaned_data["Time"]
            calendar_index = helpers.cal_index(day, time)
            
            # Convert new lines to html
            description = description.replace("\n", "<br>")
            
            # Delete from database if there was a training with same calendar index
            Training.objects.filter(user = request.user, calendar_index=calendar_index).delete()


            training = Training(user=request.user, name=name, description=description, day=day, time=time, calendar_index=calendar_index)
            training.save()
            return HttpResponseRedirect(reverse("training"))
        
        else:
            # Failed to save, display page with error
            calendar_list = [None] * 69

            trainings = Training.objects.filter(user=request.user)

            # Place training on a list in accordance with the index
            for training in trainings:
                calendar_list[training.calendar_index] = training

            return render(request, "fit/training.html", {
            "add": TrainMealForm(),
            "train": calendar_list,
            "error": "Form error"
        })
        
    else:
        calendar_list = [None] * 69

        try:
            trainings = Training.objects.filter(user=request.user)
        except TypeError:
            return render(request, "fit/login.html", {
                "message": "Required to log in"
            })

        # Place training on a list in accordance with the index
        for training in trainings:
            calendar_list[training.calendar_index] = training

        return render(request, "fit/training.html", {
            "add": TrainMealForm(),
            "train": calendar_list
        })


def diet(request):
    if request.method == "POST":
        form = TrainMealForm(request.POST)
        if form.is_valid():
            # Collect values from the form
            name = form.cleaned_data["Name"]
            description = form.cleaned_data["Description"]
            day = form.cleaned_data["Day"]
            time = form.cleaned_data["Time"]
            calendar_index = helpers.cal_index(day, time)

            # Convert new lines to html
            description = description.replace("\n", "<br>")
            
            # Delete from database if there was a training with same calendar index
            Meal.objects.filter(user = request.user, calendar_index=calendar_index).delete()


            meal = Meal(user=request.user, name=name, description=description, day=day, time=time, calendar_index=calendar_index)
            meal.save()
            return HttpResponseRedirect(reverse("diet"))
        
        else:
            # Failed to save, display page with error
            calendar_list = [None] * 69

            meals = Meal.objects.filter(user=request.user)

            # Place training on a list in accordance with the index
            for meal in meals:
                calendar_list[meal.calendar_index] = meal

            return render(request, "fit/diet.html", {
            "add": TrainMealForm(),
            "meal": calendar_list,
            "error": "Form error"
        })
        
    else:
        calendar_list = [None] * 69

        try:
            meals = Meal.objects.filter(user=request.user)
        except TypeError:
            return render(request, "fit/login.html", {
                "message": "Required to log in"
            })

        # Place training on a list in accordance with the index
        for meal in meals:
            calendar_list[meal.calendar_index] = meal

        return render(request, "fit/diet.html", {
            "add": TrainMealForm(),
            "meal": calendar_list
        })

def records(request):
    if request.method == "POST":
        form = CardioForm(request.POST)
        if form.is_valid():
            # Collect values from the form
            date = form.cleaned_data["Date"]
            time = form.cleaned_data["Time"]
            distance = form.cleaned_data["Distance"]
            discipline = form.cleaned_data["Discipline"]

            # Calculate average speed
            hours = time / 60
            speed = distance/hours
            speed = "{:.2f}".format(speed)

            cardio = Cardio(user=request.user, date=date, time=time, distance=distance, discipline=discipline, speed=speed)
            cardio.save()
            return HttpResponseRedirect(reverse("records"))    
        else:
            return HttpResponseRedirect(reverse("records"))  

    else:
        try:
            cardios = Cardio.objects.filter(user=request.user).order_by('-date')
        except TypeError:
            return render(request, "fit/login.html", {
                "message": "Required to log in"
            })
        paginator = Paginator(cardios, 30) 

        page_number = request.GET.get('page')
        cardios = paginator.get_page(page_number)

        return render(request, "fit/records.html", {
            "add": CardioForm(),
            "cardios": cardios
        })

def measurements(request):
    if request.method == "POST":
        form = MeasurementForm(request.POST)
        if form.is_valid():
            # Collect values from the form
            date = form.cleaned_data["Date"]
            weight = form.cleaned_data["Weight"]
            waist = form.cleaned_data["Waist"]
            chest = form.cleaned_data["Chest"]
            thigh = form.cleaned_data["Thigh"]
            arm = form.cleaned_data["Arm"]
            notes = form.cleaned_data["Notes"]
            notes = notes.replace("\n", "<br>")


            new_measurement = Measurement(user=request.user, date=date, weight=weight, waist=waist, 
            chest=chest, thigh=thigh, arm=arm, notes=notes)
            new_measurement.save()
            return HttpResponseRedirect(reverse("measurements"))    
        else:
            return HttpResponseRedirect(reverse("measurements"))  

    else:
        try:
            user_measurements = Measurement.objects.filter(user=request.user).order_by('-date')
        except TypeError:
            return render(request, "fit/login.html", {
                "message": "Required to log in"
            })
        paginator = Paginator(user_measurements, 30) 

        page_number = request.GET.get('page')
        user_measurements = paginator.get_page(page_number)

        return render(request, "fit/measurements.html", {
            "add": MeasurementForm(),
            "user_measurements": user_measurements
        })

def show_training(request, training_id):
    # Query for requested training
    try:
        training = Training.objects.get(pk=training_id)
    except Training.DoesNotExist:
        return JsonResponse({"error": "Training not found."}, status=404)
    
    if request.method == "GET":
        return JsonResponse(training.serialize())
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)
    
def show_meal(request, meal_id):
    # Query for requested meal
    try:
        meal = Meal.objects.get(pk=meal_id)
    except Meal.DoesNotExist:
        return JsonResponse({"error": "Meal not found."}, status=404)
    
    if request.method == "GET":
        return JsonResponse(meal.serialize())
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)

@csrf_exempt 
def delete_training(request, training_id):
    # Query for requested training
    try:
        training = Training.objects.get(pk=training_id)
    except Training.DoesNotExist:
        return JsonResponse({"error": "Training not found."}, status=404)
    
    training.delete()
    return JsonResponse({"message": "Deleted successfully"}, safe=False)

@csrf_exempt 
def delete_meal(request, meal_id):
    # Query for requested training
    try:
        meal = Meal.objects.get(pk=meal_id)
    except Meal.DoesNotExist:
        return JsonResponse({"error": "Meal not found."}, status=404)
    
    meal.delete()
    return JsonResponse({"message": "Deleted successfully"}, safe=False)

def show_record(request, record_id):
    # Query for requested trainig
    try:
        record = Cardio.objects.get(pk=record_id)
    except Cardio.DoesNotExist:
        return JsonResponse({"error": "Record not found."}, status=404)
    
    if request.method == "GET":
        return JsonResponse(record.serialize())
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)
    
@csrf_exempt 
def delete_record(request, record_id):
    # Query for requested training
    try:
        cardio = Cardio.objects.get(pk=record_id)
    except Cardio.DoesNotExist:
        return JsonResponse({"error": "Record not found."}, status=404)
    
    cardio.delete()
    return JsonResponse({"message": "Deleted successfully"}, safe=False)

def show_measurements(request, measurement_id):
    # Query for requested measurements
    try:
        single_measurements = Measurement.objects.get(pk=measurement_id)
    except Measurement.DoesNotExist:
        return JsonResponse({"error": "Measurements not found."}, status=404)
    
    if request.method == "GET":
        return JsonResponse(single_measurements.serialize())
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)
    
@csrf_exempt 
def delete_measurements(request, measurement_id):
    # Query for requested training
    try:
        single_measurements = Measurement.objects.get(pk=measurement_id)
    except Measurement.DoesNotExist:
        return JsonResponse({"error": "Measurements not found."}, status=404)
    
    single_measurements.delete()
    return JsonResponse({"message": "Deleted successfully"}, safe=False)

