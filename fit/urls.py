from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("bmi", views.bmi, name="bmi"),
    path("interval", views.interval, name="interval"),
    path("training", views.training, name="training"),
    path("diet", views.diet, name="diet"),
    path("records", views.records, name="records"),
    path("measurements", views.measurements, name="measurements"),

    # API routes
    path("training/<int:training_id>", views.show_training, name="show_training"),
    path("meal/<int:meal_id>", views.show_meal, name="show_meal"),
    path("delete_training/<int:training_id>", views.delete_training, name="delete_training"),
    path("delete_meal/<int:meal_id>", views.delete_meal, name="delete_meal"),
    path("records/<int:record_id>", views.show_record, name="show_record"),
    path("delete_record/<int:record_id>", views.delete_record, name="delete_record"),
    path("measurements/<int:measurement_id>", views.show_measurements, name="show_measurements"),
    path("delete_measurements/<int:measurement_id>", views.delete_measurements, name="delete_measurements"),
]
