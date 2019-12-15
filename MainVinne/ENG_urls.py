from django.urls import path

from . import ENG_views
app_name = "MainVinne"
urlpatterns = [
    path('', ENG_views.Home.as_view(), name="eng_main"),
    path('electronConfigurator/', ENG_views.Skeemer.as_view(), name="eng_skeemer"),
    path('search/', ENG_views.search.as_view(), name="eng_search"),
    path('practise/', ENG_views.harjutama.as_view(), name="eng_harjutama"),
    path('<str:element>/', ENG_views.Element.as_view(), name="eng_element")
]