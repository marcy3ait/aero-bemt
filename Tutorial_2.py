#%% [markdown]
# ## Atividade 06
#
# Plotar o gráfico de coeficiente tração por FM considerando os paramentros
#Dados:
#
#$C_{l\alpha}$ = 5.9
#
#$\sigma = 0.1$
#
# Cd0 = 0.01
#
# d1 = 0.025
#
# d2 = 0.65
#
#$ C_{treq} $ variando de 0.001 a 0.01
#
# $\theta_{tw}$ = \[0°, -5°, -10°, -15°, -20°, -25°]
#
#%%
import aerobemt as bem
import matplotlib.pyplot as plt 
import numpy as np

ctreq = np.linspace(0.001, 0.01, 10)
twist = np.linspace(0, -25, 6)
for i in twist:
    rotor1 = bem.Rotor(cla = 5.9, solidEqui= 0.1, ctreq = ctreq, numberBlades=4, twist=i )
    #rotor1.setArrato(cd0 = 0.01, d1=0.025, d2 = 0.65 )

    simulacao = bem.Bemt(rotor1, correcao=True)
    __, __, __, __, K , __, Fmerit = simulacao.solver()
    plt.plot(ctreq[K != 0], K[ K != 0], label = f'twist = {i} [°]')

plt.show()
# %%
