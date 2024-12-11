import matplotlib.pyplot as plt
import numpy as np

# Setez dimensiunea imaginii
plt.rcParams['figure.dpi'] = 250

tensiuni = np.zeros((5, 5))
tensiuni_medii = []
tensiuni_diff = []
tensiuni_std = []


# Extrag tensiunile din fisierele de date
for i in range(2, 7):
    tensiuni[i - 2] = np.genfromtxt(f"data{i}_min.csv", delimiter=",", skip_header=1)[:, 0]

# Calculez tensiunile medii
for i in range(5):
    tensiuni_medii.append(np.mean(tensiuni[:, i]))

# Inversez tensiunile pentru a avea N crescator
tensiuni_medii = tensiuni_medii[::-1]
tensiuni_diff = np.diff(tensiuni_medii)
tensiuni_std = np.std(tensiuni, axis=1, ddof=1)

# Generez graficul
fig, ax = plt.subplots()
ax.plot(range(1, 6), tensiuni_medii, marker='o', linestyle=' ', label="Tensiune medie")
ax.set_xlabel("N")
ax.set_ylabel("Tensiune medie [V]")
ax.set_title("Tensiunea medie in functie de N")

# Regresie liniara s
coef = np.polyfit(range(1, 4), tensiuni_medii[0:3], 1)
panta_s = coef[0]
ax.plot(range(1, 4), np.polyval(coef, range(1, 4)), linestyle='--', color='red', label="Regresie liniara s")

# Regresie liniara p
coef = np.polyfit(range(3, 6), tensiuni_medii[2:5], 1)
panta_p = coef[0]
ax.plot(range(3, 6), np.polyval(coef, range(3, 6)), linestyle='--', color='green', label="Regresie liniara p")

# Calculez panta
coef = np.polyfit(range(1, 6), tensiuni_medii, 1)
panta = coef[0]
print(f"Energie: {panta}")

# Calculez energiile
h = 6.626e-34
c = 3e8
e = 1.602e-19
E_s = panta_s * e  # [J]
E_p = panta_p * e  # [J]

fig.legend()
fig.savefig("tensiuni_medii.png")


# Generez graficul diferentei de tensiune
fig, ax = plt.subplots()
n_diff = [1.5, 2.5, 3.5, 4.5]
ax.plot(n_diff, tensiuni_diff, marker='o', linestyle=' ', label="Diferenta de tensiune")
ax.set_xlabel("N")
ax.set_ylabel("Diferenta de tensiune [V]")
ax.set_title("Diferenta de tensiune in functie de N")

fig.legend()
fig.savefig("tensiuni_diff.png")


wavelength_3p_3s = h * c / (E_p - E_s) * 1e9  # nm
wavelength_3s_2s = h * c / E_s * 1e9  # nm

print(f"Energie s: {panta_s}")
print(f"Energie p: {panta_p}")
print(f"Lungime de unda p-s: {wavelength_3p_3s:.2f} nm")
print(f"Lungime de unda s-s: {wavelength_3s_2s:.2f} nm")
print(tensiuni_std)