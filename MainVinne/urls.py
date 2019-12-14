from django.urls import path

from . import views
app_name = "MainVinne"
urlpatterns = [
    path('', views.MainSite.as_view(), name="main"),
    path('result/', views.Results.as_view(), name="results"),
    path('search/', views.search.as_view(), name="search"),
    path('<str:element>/', views.Element.as_view(), name="element")


]