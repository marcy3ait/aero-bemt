# Implementação

O software foi implementado usando a técnica de POO (Programação Orientado a Objeto), duas classes foram implementadas. Uma das classes define as caracteristicas do rotor e a outra define as caracteristicas da simulação.


## Rotor  

``class Rotor(parametros):``

Classe onde são definida as caracteristicas do rotor.



### Parâmetros: 
Parâmetros que definem o rotor, para mais detalhes sobre como definir o rotor ver o tutorial.
      
#### Parâmetros obrigatorios [Tipo de dado] [unidade] [default]
    cla: Inclinação da curva cl X aoa [double] [1/rad]
    solidEqui: Solidez equivalente do rotor [double] 
    gamma: Razão de afilamento (gamma:1) [double] [default gamma = 1]
    offset: Região cutout [double] [default offset = 0.1] 
    numberBlades: Número de pás [double]
    ctreq: Coeficiente de tração requerida [double] 
    twist: Distrição de torção ao longo do raio [double] [deg]
        
#### Parâmetros opcionais 
    
    Parâmetros do coef. de arrasto parasita
    cd0: coeficiente de arrasto [double] [default cd0 = 0]
    d1: Parametro de arrasto d1*aoa [double] [default d1 = 0]
    d2: Parametro de arrasto d2*aoa² [double] [default d2 = 0]
        


## Bemt

``class Bemt(parametros):``

Classe onde são definidas as caracteristicas da simulação e onde são implementado os métodos (funções) para o solver.

### Parâmetros
    rotor: classe rotor
    correcao: correção de ponta de pá [booleano] [default correcao = False]
    elementosPa: número de elementos de pá [int] [default elementosPa = 100]

### Método
    Solver: Método principal 
    -> falar sobre a convergencia da velocidade
    -> comentar que para ct pequenos e angulos de torção a solução pode não convergir, pq o metodo não captura sustentação negativa.

### Output
Lista completa dos output das simulação.

    dct_dr: Gradiente do coeficiente de tração.
    dcq_dr: Gradiente do coeficiente de torque.
    vel_ind: Velocidade induzida.
    cl: Coeficiente de sustentação.
    k: Fator de pontencia induzida.
    cp: Coeficiente de potência total.
    Fmerit: Figura de mérito (razão entre potecia ideal e potencia total).

### Exemplo (ver tutorial)
    # Definindo rotor
    rotorTeste = Rotor(cla = 5.9, ctreq = Ctreq, solidEqui = 0.1, numberBlades = 2, twist = theta_dis )
    # Definindo parametros de arrasto
    rotorTeste.setArrato(cd0 = 0.01, d1 = 0.025 , d2 = 0.65)
    # Definindo parametro de afilamento
    rotorTeste.setAfilamento(gamma = 2)

    # Definindo simulação
    simula = Bemt( rotorTeste, correcao = True)
    # output
    dct_dr, dcq_dr, vel_ind, cl, k, cp, Fmerit = simula.solver()