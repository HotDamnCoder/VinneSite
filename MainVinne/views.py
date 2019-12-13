from .Generate_Table import *
from .elements import ELEMENTS
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import View
from django.urls import reverse
import re

class MainSite(View):
    def get(self, request):
        return render(request, "MainVinne/VinneHTML/Vinne.html", {})


class Results(View):
    def get(self, request):
        return render(request, "MainVinne/VinneHTML/Result.html", {})

    def post(self, request):
        try:

            electrons = int(request.POST["Elektron"])
            if electrons == 0:
                raise ValueError
            orbital_amount = generate_orbital_needs(electrons)
            orbital_names = generate_orbital_layer_names(0, orbital_amount)
            table = generate_table(orbital_names[:])
            orb_values = generate_orbital_values(orbital_names)
            electron_sch = create_electron_scheme(table, electrons, orb_values)
            print(len(ELEMENTS))
            if electrons <= len(ELEMENTS):
                element = ELEMENTS[electrons]
            else:
                element = "Doesn't exist"
            Last_electrons, Nr_of_shells, element_kind, square_scheme = read_electron_scheme(electron_sch, orb_values)
            text = ""
            for scheme in square_scheme:
                text += scheme+"\n"
            context = {"elektronid": electrons, "element": element, "kihid": Nr_of_shells, "tüüp": element_kind, "eskeem": electron_sch, "rskeem": text}
            return render(request, "MainVinne/VinneHTML/Result.html", context)
        except ValueError:
            return render(request, "MainVinne/VinneHTML/Result.html", {})


class Element(View):
    def get(self, request, element, electrons):
        name = element+str(electrons)
        new_name = re.split(r'(\d)', name, 1)[0]
        electrons = int("".join(re.split(r'(\d)', name, 1)[1:]))
        element = vars(ELEMENTS[electrons])
        print(element)
        element["nimi"] = new_name
        return render(request, "MainVinne/VinneHTML/Element.html", element)


"""number : int
Atomic number
symbol : str of length 1 or 2
Chemical symbol
name : str
Name in english
group : int
Group in periodic table
period : int
Period in periodic table
block : int
Block in periodic table
series : int
Index to chemical series
protons : int
Number of protons
neutrons : int
Number of neutrons in the most abundant naturally occurring stable
isotope
nominalmass : int
Mass number of the most abundant naturally occurring stable isotope
electrons : int
Number of electrons
mass : float
Relative atomic mass. Ratio of the average mass of atoms
of the element to 1/12 of the mass of an atom of 12C
exactmass : float
Relative atomic mass calculated from the isotopic composition
eleneg : float
Electronegativity (Pauling scale)
covrad : float
Covalent radius in Angstrom
atmrad :
Atomic radius in Angstrom
vdwrad : float
Van der Waals radius in Angstrom
tboil : float
Boiling temperature in K
tmelt : float
Melting temperature in K
density : float
Density at 295K in g/cm3 respectively g/L
oxistates : str
Oxidation states
eleaffin : float
Electron affinity in eV
eleconfig : str
Ground state electron configuration
eleconfig_dict : dict
Ground state electron configuration (shell, subshell): electrons
eleshells : int
Number of electrons per shell
ionenergy : tuple
Ionization energies in eV
isotopes : dict
Isotopic composition.
keys: isotope mass number
values: Isotope(relative atomic mass, abundance)
"""






