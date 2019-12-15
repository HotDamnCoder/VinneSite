from django.urls import path

from . import views
app_name = "MainVinne"
urlpatterns = [

    path('ee/', views.MainSite.as_view(), name="main"),
    path('ee/result/', views.Results.as_view(), name="results"),
    path('ee/search/', views.search.as_view(), name="search"),
    path('ee/harjutamine/', views.harjutama.as_view(), name="harjutama"),
    path('ee/<str:element>/', views.Element.as_view(), name="element")


]