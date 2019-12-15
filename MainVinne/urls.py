from django.urls import path

from . import views
app_name = "Global_MainVinne"
urlpatterns = [
    path('', views.redirect.as_view(), name="redirect")
]