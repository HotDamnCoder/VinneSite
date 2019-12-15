from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View
from MainVinne.Functions.skeemer_context import skeemer_context
from MainVinne.Functions.generate import generate
from MainVinne.Functions.corrected_skeem import correct_skeem
from .models import Element as Elements


class Home(View):
    @staticmethod
    def get(request):
        return render(request, "MainVinne/VinneHTML/EST_html/home_EST.html", {})


class Skeemer(View):
    @staticmethod
    def get(request):
        return render(request, "MainVinne/VinneHTML/EST_html/elektronSkeemer_EST.html", {})

    @staticmethod
    def post(request):
        error = False
        try:
            electrons = int(request.POST["Elektron"])
            if electrons == 0:
                raise ValueError
        except ValueError:
            ele = request.POST["Element"]
            try:
                electrons = Elements.objects.get(est_name__iexact=ele)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                try:
                    electrons = Elements.objects.get(symbol__iexact=ele).electrons
                except ObjectDoesNotExist:
                    error = True
                    return render(request, "MainVinne/VinneHTML/EST_html/elektronSkeemer_EST.html", {"error": error})
        try:
            element = Elements.objects.get(number=electrons).est_name
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            element = "Ei eksisteeri"
        electron_sch, orb_values = generate(electrons)
        context = skeemer_context(electron_sch, orb_values)
        context["error"] = error
        context["elektronid"] = electrons
        context["element"] = [element]
        return render(request, "MainVinne/VinneHTML/EST_html/elektronSkeemer_EST.html", context)


class Element(View):
    @staticmethod
    def get(request, element):
        try:
            element = Elements.objects.get(est_name__iexact=element)
        except ObjectDoesNotExist:
            raise Http404
        return render(request, "MainVinne/VinneHTML/EST_html/element_EST.html", vars(element))


class search(View):
    @staticmethod
    def post(request):
        query = request.POST["query"]
        try:
            results = Elements.objects.filter(number=int(query))
        except ValueError:
            results = Elements.objects.filter(symbol__iexact=query) | Elements.objects.filter(est_name__icontains=query)
        return render(request, "MainVinne/VinneHTML/EST_html/search_EST.html", {"results":results})


class harjutama(View):
    @staticmethod
    def post(request):
        inskeem = request.POST["inskeem"]
        inelement = request.POST["inelement"]
        inskeem = inskeem.strip()
        inelement = inelement.strip()
        orbitals = inskeem.split(" ")
        print(inelement)
        try:
            electrons = Elements.objects.get(est_name__iexact=inelement).electrons
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            try:
                electrons = Elements.objects.get(symbol__iexact=inelement).electrons
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                return render(request, "MainVinne/VinneHTML/EST_html/harjutamine_EST.html", {"error" : True})
        html = correct_skeem(electrons, orbitals)
        return render(request, "MainVinne/VinneHTML/EST_html/harjutamine_EST.html",
                      {"html": html, "element": inelement, "skeem": inskeem})

    @staticmethod
    def get(request):
        return render(request, "MainVinne/VinneHTML/EST_html/harjutamine_EST.html", {})






