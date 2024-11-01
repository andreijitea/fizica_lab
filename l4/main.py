import matplotlib.pyplot as plt
import numpy as np

# Setez rezolutia imaginii
plt.rcParams['figure.dpi'] = 250

# Densitatile pentru fiecare metal
densitati = {'Al': 2.7, 'Fe': 7.8}

for i in {'Al', 'Fe'}:
    # Extrag datele din experiment pentru metalul 'i'
    data = np.genfromtxt(f"data_{i.lower()}.csv", delimiter=",", skip_header=1)
    # Calculez ln(n) pentru fiecare 'n
    data_ln = np.log(data[:, 1])
    # Generez graficul pentru metalul 'i'
    fig, ax = plt.subplots()
    ax.plot(data[:, 0], data_ln, linestyle=" ", marker="o")
    ax.set_title(f"Coeficient de atenuare masica pentru {i}")
    ax.set_xlabel("Grosime (cm)")
    ax.set_ylabel("ln(n)")

    # Calculez coeficientii pentru dreapta de regresie
    coef = np.polyfit(data[:, 0], data_ln, 1)
    poly1d_fn = np.poly1d(coef)
    ax.plot(data[:, 0], poly1d_fn(data[:, 0]), "--")

    # Afisez coeficientii de atenuare masica
    ax.plot([], [], ' ', label=f"μ/ρ = {-coef[0]/densitati[i]:.4f} cm^2/g")

    plt.legend()
    plt.savefig(f"plot_{i}.png")
