#%%
import matplotlib.pyplot as plt
# importando o modulo implementado
import aerobemt as bemt



# definindo um rotor


rotorTeste1 = bemt.Rotor(cla = 5.9, ctreq = [0.008] , solidEqui = 0.1,
                         numberBlades = 2, twist = -10, offset = 0.1)

# definindo parametros extras (não obrigatórios)
## parametro de afilamento
rotorTeste1.setAfilamento( gamma=2 )
## parametro de arrasto
rotorTeste1.setArrato( cd0 = 0.01, d1 = 0.025, d2 = 0.65 )

# definindo parametros da simulação

simulacao = bemt.Bemt(rotor = rotorTeste1, correcao = True, twistIdeal = False,
                     elementosPa = 200)

# realizando simulação (outputs)
dct_dr, dcq_dr, vel_ind, cl, k, cp, Fmerit = simulacao.solver()


# plotando dados 
plt.title('Velocidade induzida')
plt.plot(simulacao.r_adim, vel_ind[0,:], label = 'com correcao - 2 blades')
plt.legend()
plt.grid()
plt.show()

# %%
