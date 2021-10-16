# BEMT

## Index:
- Detalhes da implementação: [Implementação](https://github.com/marcy3ait/ProjetoFinal/blob/master/Implementa%C3%A7%C3%A3o.md)
- Detalhes de uso: [Tutoriais](https://github.com/marcy3ait/aero-bemt/blob/master/Tutorial_1.ipynb)

## Introdução: 
Implementação númerica da teoria BEMT, Blade Element Momentum Theory, para rotores  verticais de hélicopteros em voo pairado. Para ver detalhes de uso do modulo veja os tutoriais.

A teoria BEMT é a combinação de duas outras teorias, a teoria da quantidade de movimento ou teoria do disco atuador e a teoria do elemento de pá (BET - Blade Element Theory).

A teoria da quantidade de movimento modela
 o rotor com um disco atuador (um rotor com número infinito de pás) com espessura despressível que suporta a diferença de pressão que gera a sustentação, sem agregar ao modelo caracteristicas de projeto da hélice. Contudo, essa simples teoria fornece alguns parametros de desempenho do rotor baseando-se na leis de conservação de momento do fluido em um volume de controle que engloba o rotor. 

A BET assume que a pá é composta de pequenos elementos bidimensionais, aerofólios, que são submetidos ao escoamento de forma a gerar forças e momentos que são integradas na pá para compor as forças globais. Para mais detalhes da implementação consultar [relátorio final](https://github.com/marcy3ait/aero-bemt/blob/master/Relatorio_aerodinamica_helicopteros.pdf).

## Características da implementação: 

- Correção de ponta de pá (Modelo de Prandtl);
- Afilamento da pá (Poderado pela tração);
- Polar de arrasto parabolica;
- Torção linear da pá;
- Torção ideal.


## limitações:
- Não há correção de compressibilidade;
- Modelo não preve sustentação negativa;
- Modelo não preve interferencia das pás no escoamento; 



## Referencias:
[LEISHMAN2000]	Leishman, J.G. 2000. Principles of Helicopter Aerodynamics. Cambridge University Press.
