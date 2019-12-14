from .Generate_Table import *
from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Element as Elements
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

class MainSite(View):
    def get(self, request):
        return render(request, "MainVinne/VinneHTML/Vinne.html", {})


class Results(View):
    def get(self, request):
        return render(request, "MainVinne/VinneHTML/Result.html", {})

    def post(self, request):
        error = False
        try:
            electrons = int(request.POST["Elektron"])
            if electrons == 0:
                raise ValueError
            orbital_amount = generate_orbital_needs(electrons)
            orbital_names = generate_orbital_layer_names(0, orbital_amount)
            table = generate_table(orbital_names[:])
            orb_values = generate_orbital_values(orbital_names)
            electron_sch = create_electron_scheme(table, electrons, orb_values)
            try:
                element = Elements.objects.get(number=electrons).name
            except ObjectDoesNotExist:
                element = "Doesn't exist"
            Last_electrons, Nr_of_shells, element_kind, square_scheme = read_electron_scheme(electron_sch, orb_values)
            text = ""
            for scheme in square_scheme:
                text += scheme+"\n"
            context = {"error": error, "elektronid": electrons, "element": element, "kihid": Nr_of_shells, "tüüp": element_kind, "eskeem": electron_sch, "rskeem": text}
            return render(request, "MainVinne/VinneHTML/Result.html", context)
        except ValueError:
            error = True
            return render(request, "MainVinne/VinneHTML/Result.html", {"error": error})


class Element(View):
    def get(self, request, element):
        try:
            element = Elements.objects.get(name=element)
        except ObjectDoesNotExist:
            raise Http404
        return render(request, "MainVinne/VinneHTML/Element.html", vars(element))

class search(View):
    def post(self, request):
        query = request.POST["query"]
        try:
            results = Elements.objects.filter(number=int(query))
        except ValueError:
            results = Elements.objects.filter(name__contains=query)
        return render(request, "MainVinne/VinneHTML/search.html", {"results":results})







