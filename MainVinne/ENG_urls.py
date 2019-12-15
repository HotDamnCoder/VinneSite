from django.urls import path

from . import ENG_views
app_name = "MainVinne"
urlpatterns = [
    """
    path('', ENG_views.Home.as_view(), name="main"),
    path('result/', ENG_views.Results.as_view(), name="results"),
    path('search/', ENG_views.search.as_view(), name="search"),
    path('harjutamine/', ENG_views.harjutama.as_view(), name="harjutama"),
    path('<str:element>/', ENG_views.Element.as_view(), name="element")"""
]