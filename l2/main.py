import matplotlib.pyplot as plt
import numpy as np

# Constante folosite
e = 1.602 * 10 ** (-19) # Coulomb
m = 9.109 * 10 ** (-31) # Kilogram
h = 6.625 * 10 ** (-34) # Joule * secunda
L = 0.135 # metri

d1 = 2.13 * 10 ** -10 # metri
d2 = 1.23 * 10 ** -10 # metri

# Setez dimensiunea imaginilor
plt.rcParams['figure.dpi'] = 200


# Citesc datele din fisier
data = np.loadtxt("content.csv", delimiter=",", dtype=str)
tensiuni = data[1:, 0].astype(float) # volti
Diametre1 = data[1:, 1].astype(float) # metri
Diametre2 = data[1:, 2].astype(float) # metri

# Calculez lungimea de unda
for i in range(len(tensiuni)):
    lambda1_exp = (d1 * Diametre1[i]) / (2 * L)
    lambda2_exp = (d2 * Diametre2[i]) / (2 * L)
    lambda_t = h / np.sqrt(2 * m * e * tensiuni[i])

# Calculez 1/sqrt(U)
inv_tensiuni = 1 / np.sqrt(tensiuni)

# Reprezint diametrele D1 si D2 in functie de 1/sqrt(U)
for i in range(1, 3):
    fig, ax = plt.subplots()
    ax.plot(inv_tensiuni, data[1:, i].astype(float), label=f"D{i}", marker="o", linestyle=" ")

    # Calculez dreapta de regresie
    coef = np.polyfit(inv_tensiuni, data[1:, i].astype(float), 1)

    # Afisez dreapta de regresie
    ax.plot(inv_tensiuni, coef[0] * inv_tensiuni, label=f"Dreapta de regresie pentru D{i}")

    # Calculez constantele de retea folosind panta dreptei de regresie (coef[0])
    d_exp = (2 * h * L) / (coef[0] * np.sqrt(2 * m * e))
    d_exp_round = f"{d_exp:.3e}"
    ax.plot([], [], ' ', label=f"Constanta de retea pentru D{i}: {d_exp_round} m")

    # Adaug informatii suplimentare pe grafic
    ax.set_xlabel("1/sqrt(U)")
    ax.set_ylabel(f"D{i}")
    ax.set_title(f"D{i} in functie de 1/sqrt(U)")
    ax.legend()

    # Salvez graficul
    fig.savefig(f"D{i}_1_sqrt_U.png")
