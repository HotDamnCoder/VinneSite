from django.urls import path

from . import EST_views
app_name = "MainVinne"
urlpatterns = [
    path('', EST_views.Home.as_view(), name="est_main"),
    path('elektronSkeemer/', EST_views.Skeemer.as_view(), name="est_skeemer"),
    path('otsing/', EST_views.search.as_view(), name="est_search"),
    path('harjutamine/', EST_views.harjutama.as_view(), name="est_harjutama"),
    path('<str:element>/', EST_views.Element.as_view(), name="est_element")
]