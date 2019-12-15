from django.views.generic import View
from django.shortcuts import redirect
from django.urls import reverse
class redirect(View):
    def get(self, request):
        return redirect(reverse("MainVinne:eng_main"))
