from django.urls import path

from . import EST_views
app_name = "MainVinne"
urlpatterns = [
    path('', EST_views.Home.as_view(), name="main"),
    path('elektronSkeemer/', EST_views.Skeemer.as_view(), name="results"),
    path('otsing/', EST_views.search.as_view(), name="search"),
    path('harjutamine/', EST_views.harjutama.as_view(), name="harjutama"),
    path('<str:element>/', EST_views.Element.as_view(), name="element")
]