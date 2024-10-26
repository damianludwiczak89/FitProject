

# FITProject

http://fitproject.pythonanywhere.com - sometimes loads on a 2nd time, server side issue

## Video Demo: https://youtu.be/pqqkzec3ecU

## Setup

```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Go to provided link (http://127.0.0.1:8000/ by default)

## Introduction

As stated on the main page of the website itself - FITProject was created as a final project for CS50 Web Programming with Python and Javascript course. The idea behind this project was to provide a several tools that helps users get and stay fit, keep track of progress, and use during training itself. Users after creating an account have access to calendars where they can set their weekly trainig plan, and weekly diet. There is also a table to submit cardio training results including running and cycling. Another feature is ability to keep track of body changes by providing current weight and body measurements to create a history of one's journey that helps to notice the results of hard work. Website also offers two tools that do not require an account - Body Mass Index calculator, and timer for interval training (High Intensity Interval Training).

## Distinctiveness and Complexity

Project relies heavily on tools and techniques acquired during the course. However, nature of this website provided some new challenges as described in paragraphs below. 

### High Intensity Interval Training Timer

One of my main goals was to practice further JavaScript, and the interval training timer proved to be a difficult task. There are basically two countdown timers - one for high intensity training called work, and the other for medium intensity training called rest. There is also a third value of interval counts. When one timer reaches zero, the other one starts, when the second one reaches zero, the first one is reset and starts again. Interval count is being decremented when work timer starts from beginning. 

Each value is for user to set. The JavaScript for this is based on SetInterval built-in function. To have two timers, I needed two functions - one for work, and one for rest, and two SetInverals to trigger these functions. When timer reaches 0, function has to stop current SetInterval, and trigger SetInverval for the other function, and then the other way round. Here I had a lot of scope difficulties, where one function not was not accessing SetInterval of the other function and vice versa. Designing this was very challenging. 

On top of that, I wanted to have a Stop and Pause button, accordingly to reset timers and to pause them and have the option to resume them. These buttons are available no matter which timer is currently active, so I had to add them to both functions - work and rest. 

There are also some user-friendly touches. Whenever one timer reaches zero, there is a sound informing about that, and also a different sound when the training is finished (sound source: https://www.fesliyanstudios.com/). Additionally, the timer that is currently active has a green font but I wanted to make it even more distinctive so I added CSS animations - the active timer grows a bit. That was another difficult part. Making timer grow was easy but shrinking it and growing the other one was definitely harder for me. I spent some time trying to figure out how to run animation backwards. Eventually, managed to solve it by having one animation for grow and another one for shrink, and setting runs and stops for them in right places. There is also a "Great Job!" text displayed at the end of training that also grows. 

### Body Mass Index Calculator

Popular calculator where users provide their body weight and height to get the BMI - a value that indicates if someone has a regular body weight, overweight or underweight. That tool is also based on JavaScript altough not as complicated as with HIIT timers. Two values are used in a simple math formula. Result is being displayed as a number with a written status, also font color indicates the result - green as the best, yellow one step worse, red and darker red as next steps of worse result.

### Training and Diet Calendars

Logged in users gain access to a calendar where they can set their training plan and diet for a full week. Calendar displays each day of the week with specified hours of the day. There is a button above to add training/meal, after pressing it JavaScript code is set to display a form. Here user is asked to provide a name (of training or meal), description (for example how many sets and repetitions for some exercise, or in case of a meal - ingriedients, nutritions, kcal), and also time and day from dropdown lists. Submitting the form triggers function in views (training or diet), where data is being collected and saved into database. 

The problem I had was with correctly displaying the values from database in the correct places of the calendar. When I get the QuerySet of trainings, I send it to html, but when I make a Jinja loop to unfold these vales from QuerySet, they are being put in the calendar table from the beginning, one by one. Therefore first element of the QuerySet was always displayed on Monday morning, even though it could have been set to somewhere else by the user. To solve this, I assigned an index to each calendar field, a kind of id. On the backend I created a helper function, whenever user submits new training/meal, it calls a function that takes the chosen day and time, and returns an index. Then, to display the calendar, I created an empty list of 69 elements (same number as calendar fields), then I get the QuerySet of training/meals, and I append each element of this QuerySet to the right place in this list using the calendar index value. As a result, I get a list of 69 elements, but some of them are empty, and some of them store a value. When I send this list to html, I can use a Jinja loop over the calendar table, and the data is being laid in right places, leaving empty fields if there is no value there.

When user already has some elements added to the calender, it is possible to click on them, resulting in JavaScript code displaying description for this training/meal above the calendar. That was made using fetch with GET method. As each calendar field has an index assigned, I used that value as an argument to the fetch function so the right training/meal is received. Beneath the displayed description, there is also a field to hide it, or to delete it from the calendar. Deleting is also made by fetching. Adding new training/meal to a field that already stored some data means replacing it with new entry.

### Cardio records

Another feature for logged in users is a possibility to add a cardio training, choosing from running or cycling. There is a button above that displays the form to fill. User is asked to specify date, time, distance and discipline from a dropdown list. When form is submitted, data are being stored in database, with additionaly calculated average speed. Elements are displayed on the page from the newest on top. There is also pagination used. Again, clicking on a specific training in table results in fetching that displays data from this training above the table - there user has an option to delete that entry or to hide the training back. Deleting is also made by fetching. Pagination is included to add a page every 30th entry.

### Measurements

Last tool available for logged in user is a table to keep track of body measurements. Again, there is a button above to display the form via JavaScript. Only date and weight are required to submit the data - measurements of waist, chest, thigh, and arm are optional. Submitting form calls function in views to store these values in database. Then, they are displayed again in a form of table, from the latest on top. When user clicks particular entry, data for this object is fetched and it appears above. There is also an option to delete it or hide. Deleting is also made by fetching, without reloading the page. Pagination is included to add a page every 30th entry.

### Styles

Another area to practice for me was using CSS. Unfortunately, as aesthetic design is not my strength, only some styles are applied. Most elements are centered with a grey box in the background with set margins as a border for that box. Buttons are slightly rounded, with a green shadow to match the nav-bar. Buttons and tables are mainly from Bootstrap. There are also CSS animations on HIIT timer page, as mentioned before.  


## Technologies

- Django (Python, sqlite3)
- HTML
- CSS
- JavaScript
- Bootstrap 

## Files

Project contains mostly default Django files and structures, modifying mainly views.py, urls.py, and models.py. Besides that, I crated several HTML templates and JavaScript files.

### HTML

- bmi.html - HTML template for BMI page
- diet.html - HTML template for diet calendar page
- index.html - HTML template for main page
- interval.html - HTML template for Interval Timer page
- layout.html - HTML template for layout that other templates use
- login.html - HTML template for login page
- measurements.html - HTML template for measurement history page
- records.html - HTML template for cardio history page
- register.html - HTML template for register page
- training.html - HTML template for training calendar page

### JavaScript

- bmi.js - JavaScript for bmi page
- calendar_diet.js - JavaScript for diet calendar page
- calendar_train.js - JavaScript for training calendar page
- interval.js - JavaScript for Interval Timer page
- measurements.js - JavaScript for measurement history page
- records.js - JavaScript for cardio history page

### CSS

- styles.css - CSS for whole website

### Python

- helpers.py - created to store helpers functions, however, turned out to have only one function at the moment - function that returns calendar index for Training or Meal for right calendar placement, as described earlier. More functions may be added in the future.

### Database

#### Models for this website include: User, Training, Meal, Cardio, and Measurement. 

#### User

User is a default AbstractUser model from Django without any additional fields. 

#### Training and Meal

Training and Meal models are built with same design. Each Training and Meal are related to the user that created them in order to make an individual weekly plan of training or diet. These two models store information about name of training/meal, description about it, what time and day they should be assigned to. There is also an IntegerField called calendar_index - this is a value not provided by the user but calculated by a function that on the basis of input day and time returns a number that corresponds to a field in a calendar. Having that calendar index for each training or meal makes it easier to display existing objects on the calendar in the right place.

#### Cardio

Cardio model is to store records of running and cycling. Each Cardio object is related to user that created it. It contains CharField called discipline to specifiy whether user is adding data about running or cycling. That is to choose from a dropdown list where only these two options are available. Besides that, user provides a date - using a DateField -, time (duration of training), and distance. Average speed is also stored, calculated automatically.

#### Measurement

Measurement model is to store user's body weight and measurements. It is related to user that created it. It contains date as a DateField, series of DecimalFields to store weight and measurements of waist, chest, thigh, and arm. User do not have to fill each field in order to submit data. There is also an optional field for notes as a CharField.

## Usage

Use the standard `python manage.py runserver` command to run the application. No need for any additional packages or set up.