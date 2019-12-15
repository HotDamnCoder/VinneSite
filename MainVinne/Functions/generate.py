from .Generate_Table import *


def generate(electrons):
    orbital_amount = generate_orbital_needs(electrons)
    orbital_names = generate_orbital_layer_names(0, orbital_amount)
    table = generate_table(orbital_names[:])
    orb_values = generate_orbital_values(orbital_names)
    electron_sch = create_electron_scheme(table, electrons, orb_values)
    return electron_sch, orb_values
