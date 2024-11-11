import matplotlib.pyplot as plt
import numpy as np

# Setez dimensiunea imaginilor
plt.rcParams['figure.dpi'] = 250

# Constante folosite
c = 3e8 # m/s
e = 1.6e-19 # C

# Procesez datele
U_med = []
frecv = []

for j, i in enumerate(["578", "546", "436", "405"]):
    data = np.genfromtxt(f"data_{i}.csv", delimiter=",", skip_header=1)
    wave_len = int(i) * 1e-9 # m
    frecv.append(c / wave_len) # Hz
    U_med.append(np.mean((data[:]))) # V

# Procesez datele pentru 366 nm (exclus din regresie)
wave_len_366 = 366 * 1e-9 # m
frecv_366 = c / wave_len_366 # Hz
U_med_366 = np.mean(np.genfromtxt("data_366.csv", delimiter=",", skip_header=1)) # V

# Plot
fig, ax = plt.subplots()
ax.plot(frecv, U_med, 'ro')
ax.set_xlabel("Frecventa [Hz]")
ax.set_ylabel("Tensiune [V]")

# Calculez dreapta de regresie
coef = np.polyfit(frecv, U_med, 1)
p = np.poly1d(coef)
ax.plot(frecv, p(frecv), linestyle='--')
# Calculez constanta lui Planck
h = coef[0] * e
print(f"Plank: {h:.3e} J/Hz")
ax.plot([], [], ' ', label=f"Plank: {h:.3e} J/Hz")
# Afisez valoarea pentru 366 nm
ax.plot(frecv_366, U_med_366, 'bo')

# Calculez frecventa de prag si lucrul mecanic de extractie
frecv_prag = -coef[1] / coef[0]
print(f"Frecventa de prag: {frecv_prag:.3e} Hz")
wave_len_prag = c / frecv_prag
print(f"Lambda de prag: {wave_len_prag:.3e} m")
L_extr = h * wave_len_prag
print(f"Lucrul mecanic de extractie: {L_extr:.3e} J")

ax.legend()
plt.savefig("plot.png")
