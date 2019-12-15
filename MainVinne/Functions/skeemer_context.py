from .Generate_Table import *
def skeemer_context(electron_sch, orb_values):
    Last_electrons, Nr_of_shells, element_kind, square_scheme = read_electron_scheme(electron_sch, orb_values)
    text = ""
    for scheme in square_scheme:
        text += scheme+"\n"
    context = {"kihid": Nr_of_shells, "tüüp": element_kind, "eskeem": electron_sch, "rskeem": text}
    return context