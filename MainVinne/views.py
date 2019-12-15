from django.views.generic import View
from django.shortcuts import redirect
from django.urls import reverse
from .EST_views import Home
class redirect(View):
    def get(self, request):
        return redirect(reverse(Home))
