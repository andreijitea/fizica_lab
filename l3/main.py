import matplotlib.pyplot as plt
import numpy as np

# Setez dimensiunea imaginilor
plt.rcParams['figure.dpi'] = 250

# Setez stilul de afisare
fig, ax = plt.subplots()
ax.set_ylabel('n [imp/s]')
ax.set_xlabel('E [keV]')
ax.set_title('Spectrul energetic al radiatiei beta')


# Citesc datele din tabel
data_energy = np.genfromtxt('data_energy.csv', delimiter=',', skip_header=1)
data_exp = np.genfromtxt('data_exp.csv', delimiter=',', skip_header=1)

# Extrag datele din tabel
I_exp = data_exp[:, 0] # [A]
N_exp = data_exp[:, 1] # [imp]

I_energy = data_energy[:, 0] # [A]
B_energy = data_energy[:, 1] * 1e-3 # [T]

# Constante necesare
R = 0.14 # [m]
c = 3e8 # [m/s]
m0 = 9.10938356e-31 # [kg]
q = 1.60217662e-19 # [C]

F = 121 # [imp]
t_f = 600 # [s]
f = F/t_f # [imp/s]
t = 60 # [s]

# Initializez vectorii pentru energie si numarul de particule
E = np.zeros(len(I_energy)) # [keV]
n = np.zeros(len(I_energy)) # [imp/s]

for i, I in enumerate(I_energy):
    # Calculez energia in Jouli
    E_J = np.sqrt(pow(q*R*B_energy[i]*c,2) + pow(m0,2) * pow(c,4)) - m0 * pow(c,2) # [J]
    # Transform energia in keV
    E[i] = E_J/q * 1e-3 # [keV]
    # Calculez numarul de particule
    n_p = N_exp[i] / t
    n[i] = n_p - f
    # Calculez dispersia
    dispersie = 0
    if n[i] >= 0:
        dispersie = np.sqrt(n[i]/t + f/t_f)

    # Afisez rezultatele tabelului final
    print(f'I: {I_energy[i]} A | E: {E[i]:.2f} keV | N: {N_exp[i]} | n\': {n_p:.2f} | n: {n[i]:.2f} | dispersie: {dispersie:.2f}')


# Filtrez perechile de date pentru care n >= 0
mask = n >= 0
E_filtered = E[mask]
n_filtered = n[mask]


# Calculez polinomul de interpolare de grad 5
coef = np.polyfit(E_filtered, n_filtered, 5)

# Afisez polinomul de interpolare
E_range = np.linspace(min(E_filtered), max(E_filtered), 100)
n_range = np.polyval(coef, E_range)
ax.plot(E_range, n_range, color='#FFEB0F')

# Afisez punctele calculate
ax.plot(E_filtered, n_filtered, 'o', color='#060270')

# Afisez punctul de maxim
E_h = E_range[np.argmax(n_range)]
ax.axvline(E_h, color='#7DDA58', linestyle='--', label=f'E_h = {E_h:.2f} keV')

# Afisez punctul de maxim
ax.plot([], [], ' ', label=f'E_max = {3 * E_h:.2f} keV')

plt.legend()
plt.savefig('plot.png')
