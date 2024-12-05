import matplotlib.pyplot as plt
import numpy as np

# Setez dimensiunea imaginii
plt.rcParams['figure.dpi'] = 250

data_mercur = np.genfromtxt("data_mercur.csv", delimiter=",", skip_header=1)

mercur_wl = [579, 577, 546.1, 491.6, 435.8]
mercur_inv_wl = [1 / wl**2 for wl in mercur_wl]

mercur_unghi_gr = data_mercur[:, 1]
mercur_unghi_min = data_mercur[:, 2]
mercur_unghi_total = mercur_unghi_gr + mercur_unghi_min / 60

# Grafic
fig, ax = plt.subplots()
ax.plot(mercur_unghi_total, mercur_inv_wl, 'o', label="Date experimentale")
ax.set_xlabel('Unghi [grade]')
ax.set_ylabel('1 / λ^2 [1/nm^2]')
ax.set_title("Lampa cu mercur")

# Regresie liniara
coef = np.polyfit(mercur_unghi_total, mercur_inv_wl, 1)
poly1d_fn = np.poly1d(coef)
ax.plot(mercur_unghi_total, poly1d_fn(mercur_unghi_total), '', label="Regresie liniara")
intercept = coef[1]
slope = coef[0]

date_neon = np.genfromtxt("data_neon.csv", delimiter=",", skip_header=1)
neon_unghi_gr = date_neon[:, 1]
neon_unghi_min = date_neon[:, 2]
neon_unghi_total = neon_unghi_gr + neon_unghi_min / 60

# Calcul lungimi de unda pentru neon
neon_wl = 1/np.sqrt(slope * neon_unghi_total + intercept)
print("Lungimile de unda pentru neon:")
for wl in neon_wl:
    print(f"{wl:.2f}")

ax.legend()
plt.savefig("mercur.png")