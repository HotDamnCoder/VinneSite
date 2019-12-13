import math
import re
import codecs

def generate_orbital_layer_names(starting_point, amount, characters=None, row=None):
    if row is None:
        row = []
    if characters is None:
        characters = ["s", "p", "d", "f", "g", "h", "i", "j", "k", "l", "m",
                      "n", "o", "q", "r", "t", "u", "v", "w", "x", "y"]
    generated_orbital_name = ""
    powers = []
    nr_of_char = len(characters)
    for number in range(starting_point, amount+1):
        last_generated_amount = 0
        for power in powers:
            last_generated_amount += nr_of_char ** (power + 1)
        new_generate_amount = number - last_generated_amount
        if new_generate_amount > 1:
            log = math.log(nr_of_char)
            float_log = float(math.log(new_generate_amount) / log)
            int_log = int(math.log(new_generate_amount) / log)
            if float_log == int_log:
                powers.append(len(powers))
        elif new_generate_amount == 0:
            powers.append(len(powers))
        last_generated_amount = 0
        for power in powers:
            if power == 0:
                char_number = int(number / nr_of_char ** power)
                full_loop_times = int(number / nr_of_char ** (power + 1))
            else:
                last_generated_amount += nr_of_char ** power
                char_number = int((number - last_generated_amount) / nr_of_char ** power)
                full_loop_times = int((number - last_generated_amount) / nr_of_char ** (power + 1))
            generated_orbital_name += characters[char_number - nr_of_char * full_loop_times]
        reversed_orbital_name = list(generated_orbital_name)
        reversed_orbital_name.reverse()
        generated_orbital_name = "".join(reversed_orbital_name)
        row.append(generated_orbital_name)
        generated_orbital_name = ""
    return row


def generate_table(columns_var: list, given_empty_table: list = None):
    if given_empty_table is None:
        given_empty_table = []
    first_column = []
    nr_of_colums = len(columns_var) * 2
    columns_var.insert(0, "")
    given_empty_table.append(columns_var)
    for nr in range(1, nr_of_colums):
        first_column.append(nr)
    for nr in first_column:
        row = [nr]
        given_empty_table.append(row)
    for row in given_empty_table[1:]:
        for nr in range(int(row[0])):
            if nr + 1 <= (len(columns_var)-1):
                char = str(columns_var[nr + 1])
                orbital = str(row[0]) + char
                row.insert(nr+1, orbital)
            else:
                break
    return given_empty_table


def print_table(table_fr_print: list):
    for i in table_fr_print:  # print the board
        print(i)


def read_row(starting_cord, electrons_count, ele_scheme, given_table, char_values):
    x_cord, y_cord = starting_cord
    while x_cord != 1:
        x_cord -= 1
        y_cord += 1
        value = given_table[y_cord][x_cord]
        letter = "".join(re.findall(r'[a-z]', value))
        e = char_values.get(letter)
        electrons_count -= e
        if electrons_count <= 0:
            over_e = math.fabs(electrons_count)
            e -= int(over_e)
            value += "^" + str(e)
            ele_scheme += value
            electrons_count = 0
            return y_cord, electrons_count, ele_scheme
        else:
            value += "^" + str(e) + " "
            ele_scheme += value
    return y_cord, electrons_count, ele_scheme


def create_electron_scheme(given_table, electron_count, char_values):
    x = 2
    y = 1
    if electron_count-2 < 0:
        electron_scheme = "1s^1 "
    else:
        electron_scheme = "1s^2 "
    electron_count -= 2
    while electron_count > 0:
        y_place, electron_count, electron_scheme = read_row((x, y), electron_count, electron_scheme,
                                                            given_table, char_values)
        if int(y_place / 2) == float(y_place / 2):
            x += 1
        else:
            y += 1
    return electron_scheme


def generate_orbital_needs(e):
    generated_count = 1
    current_electrons = 4
    current_orbital_count = 1
    last_multiplier = 4
    if current_electrons < e:
        current_electrons += 16
        current_orbital_count += 1
    while current_electrons < e:
        current_multiplier = last_multiplier + 5+2*generated_count
        current_electrons += 4 * current_multiplier
        current_orbital_count += 1
        generated_count += 1
        last_multiplier = current_multiplier
    return current_orbital_count


def generate_orbital_values(orbitals, orbital_values=None):
    count = 0
    if orbital_values is None:
        orbital_values = {}
    for char in orbitals:
        orbital_values[char] = 2 + 4*count
        count += 1
    return orbital_values


def read_electron_scheme(electron_scheme: str, orbital_values: dict):
    orbitals = electron_scheme.split(" ")
    if "" in orbitals:
        orbitals.remove("")
    highest_shell = 0
    e_last = 0
    for orbital in orbitals:
        new_shell = re.split(r'[a-z]', orbital)[0]
        if int(new_shell) > int(highest_shell):
            highest_shell = new_shell
    last_orbitals = orbitals[len(orbitals)-2:]
    last_orbital = last_orbitals[len(last_orbitals)-1]
    last_orbital_letter = "".join(re.findall(r'[a-z]', last_orbital))
    kind_of_element = last_orbital_letter
    for orbital in orbitals:
        if re.split(r'[a-z]', orbital)[0] == highest_shell:
            e_last += int(orbital.split("^")[1])
    square_scheme = create_square_scheme(orbitals, highest_shell, orbital_values)
    return str(e_last), highest_shell, kind_of_element, square_scheme


def write_info_to_file(electron_config, last_e, shells, kind_element, square_scheme):
    file = codecs.open("Electron configuration.txt", "w+", encoding='utf8')
    file.write("Element electron configuration: " + electron_config)
    file.write("\nElectrons in last electron shell is " + last_e)
    file.write("\nNumber of electron shells is  " + shells)
    file.write("\nElement kind is " + kind_element)
    for square in square_scheme:
        file.write("\n" + square)
    file.close()


def print_info(electron_config, last_e, shells, kind_element):
    print("Element electron configuration: " + electron_config)
    print("Electrons in last electron shell is " + last_e)
    print("Number of electron shells is  " + shells)
    print("Element kind is " + kind_element)


def add_arrow(square: str, arrow_type: int):
    if arrow_type == 0:
        return square.replace(" ", "↑", 1)
    else:
        return square.replace(" ", "↓", 1)


def create_square_scheme(orbitals: list, highest_shell: int, orbital_values:dict):
    highest_s_orbital = [orbital for orbital in orbitals if highest_shell in orbital[:-1] and "s" in orbital[:-1]]
    highest_s_orbital_index = orbitals.index(highest_s_orbital[0])
    last_orbitals = {}
    for orbital in orbitals[highest_s_orbital_index:]:
        e_count = int(orbital.split("^")[1])
        orbital_letter = "".join(re.findall(r'[a-z]', orbital))
        orbital_count = int(orbital_values.get(orbital_letter) / 2)
        empty_orbital_squares = []
        filled_once_orbital_squares = []
        filled_twice_orbital_squares = []
        for i in range(orbital_count):
            empty_orbital_squares.append("[  ]")
        for orbital_square in empty_orbital_squares:
            if e_count > 0:
                orbital_square = orbital_square.replace(" ", "↑", 1)
                e_count -= 1
            filled_once_orbital_squares.append(orbital_square)
        if e_count > 0:
            for orbital_square in filled_once_orbital_squares:
                if e_count > 0:
                    orbital_square = orbital_square.replace(" ", "↓", 1)
                    e_count -= 1
                filled_twice_orbital_squares.append(orbital_square)
        else:
            filled_twice_orbital_squares = filled_once_orbital_squares
        last_orbitals[orbital] = filled_twice_orbital_squares
    total_length = 0
    for x in last_orbitals.values():
        total_length += len(x)
    total_length *= 4
    reverse_values = list(last_orbitals.values())
    reverse_values.reverse()
    square_print_values = []
    start_location = total_length
    count = 0
    for square in reverse_values:
        square_print_value = ""
        orbital = list(last_orbitals.keys())
        orbital.reverse()
        orbital = orbital[count]
        start_location -= len(square)*4
        center = int((len(square)*4 - len(orbital)) / 2) + start_location
        for i in range(start_location):
            square_print_value += " "
        for sq in square:
            square_print_value += sq
        square_print_values.append(square_print_value)
        square_print_value = ""

        for i in range(center):
            square_print_value += " "
        square_print_value += orbital
        square_print_values.append(square_print_value)
        count += 1
    return square_print_values

