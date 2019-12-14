from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render
from django.views.generic import View

from .Generate_Table import *
from .models import Element as Elements


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
        except ValueError:
            ele = request.POST["Element"]
            try:
                electrons = Elements.objects.get(est_name__iexact=ele)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                try:
                    electrons = Elements.objects.get(name__iexact=ele).electrons
                except ObjectDoesNotExist:
                    try:
                        electrons = Elements.objects.get(symbol__iexact=ele).electrons
                    except ObjectDoesNotExist:
                        error = True
                        return render(request, "MainVinne/VinneHTML/Result.html", {"error": error})
        orbital_amount = generate_orbital_needs(electrons)
        orbital_names = generate_orbital_layer_names(0, orbital_amount)
        table = generate_table(orbital_names[:])
        orb_values = generate_orbital_values(orbital_names)
        electron_sch = create_electron_scheme(table, electrons, orb_values)
        try:
            element = Elements.objects.get(number=electrons).name
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            element = "Doesn't exist"
        Last_electrons, Nr_of_shells, element_kind, square_scheme = read_electron_scheme(electron_sch, orb_values)
        text = ""
        for scheme in square_scheme:
            text += scheme+"\n"
        context = {"error": error, "elektronid": electrons, "element": element, "kihid": Nr_of_shells, "tüüp": element_kind, "eskeem": electron_sch, "rskeem": text}
        return render(request, "MainVinne/VinneHTML/Result.html", context)


class Element(View):
    def get(self, request, element):
        try:
            element = Elements.objects.get(name__iexact=element)
        except ObjectDoesNotExist:
            raise Http404
        return render(request, "MainVinne/VinneHTML/Element.html", vars(element))

class search(View):
    def post(self, request):
        query = request.POST["query"]
        try:
            results = Elements.objects.filter(number=int(query))
        except ValueError:
            results = Elements.objects.filter(symbol__iexact=query) |\
                    Elements.objects.filter(name__icontains=query) | Elements.objects.filter(est_name__icontains=query)
        return render(request, "MainVinne/VinneHTML/search.html", {"results":results})


class harjutama(View):
    def post(self, request):
        inskeem = request.POST["inskeem"]
        inelement = request.POST["inelement"]
        inskeem = inskeem.strip()
        inelement = inelement.strip()
        orbitals = inskeem.split(" ")
        print(inelement)
        try:
            electrons = Elements.objects.get(name__iexact=inelement).electrons
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            try:
                electrons = Elements.objects.get(est_name__iexact=inelement).electrons
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                try:
                    electrons = Elements.objects.get(symbol__iexact=inelement).electrons
                except (ObjectDoesNotExist, MultipleObjectsReturned):
                    return render(request, "MainVinne/VinneHTML/harjutamine.html", {"error" : True})
        orbital_amount = generate_orbital_needs(electrons)
        orbital_names = generate_orbital_layer_names(0, orbital_amount)
        table = generate_table(orbital_names[:])
        orb_values = generate_orbital_values(orbital_names)
        electron_sch = create_electron_scheme(table, electrons, orb_values)
        electron_sch = electron_sch.split(" ")

        wrong = []
        right = []
        count = 0
        html = "<p>"
        if len(electron_sch) > len(orbitals) or len(electron_sch) == len(orbitals) :
            for y in electron_sch:
                try:
                    x = orbitals[count]
                    if x != y:
                        wrong.append(x)
                    else:
                        right.append(x)
                except IndexError:
                    wrong.append("...")
                count += 1
        else:
            for y in orbitals:
                try:
                    x = electron_sch[count]
                    if y != x:
                        wrong.append(y)
                    else:
                        right.append(y)
                except IndexError:
                    wrong.append(y)
                count += 1

        for orb in orbitals:
            if orb in wrong:
                html += "<em class='text-danger'> "+orb+"</em>"
            else:
                html += " " + orb
        if "..." in wrong:
            html += "<em class='text-danger'>" + " ..." * wrong.count("...") + "</em>"
        html += "</p>"
        return render(request, "MainVinne/VinneHTML/harjutamine.html",
                      {"html": html, "element": inelement, "skeem": inskeem})

    def get(self, request):
        return render(request, "MainVinne/VinneHTML/harjutamine.html", {})






