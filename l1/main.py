import matplotlib.pyplot as plt
import numpy as np

# Citesc datele din fisier
data = np.loadtxt("content.csv", delimiter=",", dtype=str)

# Setez dimensiunea imaginilor
plt.rcParams['figure.dpi'] = 300

# Generez 4 grafice, cate unul pentru fiecare raza
# Graficul r=2 are x < 9
# Graficul r=3 are x < 9
# Graficul r=4 are x < 5
# Graficul r=5 are x < 4
for i in range(1, 5):
    fig, ax = plt.subplots()

    # Setez titlul, label-urile si limitele axelor
    ax.set_title(f"Sarcina specifica pentru raza {i+1}cm")
    ax.set_ylabel("U [V]")
    ax.set_xlabel(r"$I^2$ [$A^2$]")
    if i == 3:
        ax.set_xlim(0, 5)
    elif i == 4:
        ax.set_xlim(0, 4)
    else:
       ax.set_xlim(0, 10)
    ax.set_ylim(0,350)

    # Extrag tensiunile si curentii pentru raza i
    tensiuni = data[1:, 0].astype(float)
    curenti = data[1:, i].astype(float)

    # Elimin valorile 0 folosind un mask
    mask = (tensiuni != 0) & (curenti != 0)
    tensiuni = tensiuni[mask]
    curenti = curenti[mask]
    curenti = np.square(curenti)
    print(tensiuni, curenti)

    # Afisez punctele aflate in urma experimentului
    ax.plot(curenti, tensiuni, label=f"Raza {i+1}cm", marker="o")

    # Calculez dreapta de regresie folosind toate punctele (1)
    coef = np.polyfit(curenti, tensiuni, 1)
    panta = coef[0]
    print(coef)
    # Afisez dreapta de regresie (1)
    ax.plot(curenti, panta*curenti, label="Dreapta de regresie 1")

    # Calculez dreapta de regresie folosind doar punctele ce nu sunt erori evidente (2)
    # Elimin doar in cazul r=3
    if i == 2:
        coef = np.polyfit(curenti[2:], tensiuni[2:], 1)
    else:
        coef = np.polyfit(curenti, tensiuni, 1)
    panta = coef[0]

    # Afisez dreapta de regresie (2)
    ax.plot(curenti, panta*curenti, label="Dreapta de regresie 2")

    # Afisez panta dreptei de regresie (2)
    ax.plot([], [], label=f"Panta: {panta:.2f}", color="white")

    # Calculez sarcina specifica folosind panta dreptei de regresie (2)
    u0 = 4 * np.pi * pow(10, -7)
    n = 154
    R = 0.2
    r = (i+1) * pow(10, -2)

    sarc = (125 * pow(R, 2) * panta) / (32 * pow(u0, 2) * pow(n, 2) * pow(r, 2))
    ax.plot([], [], label=f"Sarcina specifica: {sarc:.2e}", color="white")

    ax.legend()
    plt.show()
