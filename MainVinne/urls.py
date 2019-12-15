from django.urls import path

from . import views
app_name = "MainVinne"
urlpatterns = [
    path('', views.redirect.as_view(), "redirect")
]