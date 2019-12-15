from django.urls import path
from django.contrib.auth import views as auth_views

from . import EST_views
app_name = "Global_MainVinne"
urlpatterns = [
    path('', EST_views.Home.as_view()),


]