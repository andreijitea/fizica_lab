import matplotlib.pyplot as plt
import numpy as np

# Setez dimensiunea imaginii
plt.rcParams['figure.dpi'] = 250

# Constante necesare
D = 0.044 # [m]
S = 0.85
eps = 0.02

# Fondul
F = 450 # [imp]
f = F / 600 # [imp/s]

# Citesc datele experimentale din fisier
data = np.genfromtxt('data.csv', delimiter=',', skip_header=1)
r = data[:, 0] * 10**-2 # [m]
N = data[:, 1] # [imp]
t = 120 # [s]

n = N/t - f
unghi_solid = 1/2 - 1/(np.sqrt(4 + (D / r)**2))

# Adaug punctul (0,0)
unghi_solid = np.insert(unghi_solid, 0, 0)
n = np.insert(n, 0, 0)

# Graficul
fig, ax = plt.subplots()
ax.plot(unghi_solid, n, 'o', label='Date experimentale')
ax.set_xlabel('Unghi solid [rad]')
ax.set_ylabel('viteza [imp/s]')

# Regresia liniara
panta = np.sum(unghi_solid * n) / np.sum(unghi_solid**2)
ax.plot(unghi_solid, panta * unghi_solid, label='Regresia liniara', color='orange')

# Calculez activitatea sursei
act = panta / (S * eps)
ax.plot([], [], ' ', label=f'Activitate: {act / 1000:.2f} kBq')

ax.legend()
plt.savefig("plot.png")
