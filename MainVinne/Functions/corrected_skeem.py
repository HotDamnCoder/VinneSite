from MainVinne.Functions.generate import generate


def correct_skeem(electrons, orbitals):
    electron_sch, orb_values = generate(electrons)
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
    return html
