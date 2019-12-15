from django.urls import path
from django.views.generic.base import RedirectView
from . import EST_views
app_name = "Global_MainVinne"
urlpatterns = [
    path('', EST_views.Home.as_view())
]