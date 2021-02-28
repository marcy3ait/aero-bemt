#%%
import numpy as np 
import matplotlib.pyplot as plt 

class Rotor:

    def __init__(self, cla, ctreq, solidEqui, numberBlades, twist,   offset = 0.1):

        ''' 
            Parametros:
            cla: Inclinação da curva clXaoa
            solidEqui: Solidez equivalente do rotor
            gamma: Razão de afilamento (gamma:1)
            offset: Região cutout
            numberBlades: Número de pás
            ctreq: Coeficiente de tração requerida
            twist: Distrição de torção ao longo do raio : list [deg]
        '''

        self.cla = cla
        # definindo solidez equivalente
        self.solidEqui = solidEqui 
        self.ctreq = ctreq
        self.numberBlades = numberBlades
        self.twist = (np.pi/180)*np.array(twist)
        self.offset = offset

        # afilamento default
        self.gamma = 1

        # set default do arrasto
        self.cd0 = 0
        self.d1  = 0
        self.d2  = 0
        
    def setArrato(self, cd0 , d1 = 0, d2 = 0):

        '''
        Definição dos coeficientes da equação parabolica do arrasto
        em função do aoa.
        Parametros:
        cd0: coeficiente de arrasto 
        d1: Parametro de arrasto d1*aoa
        d2: Parametro de arrasto d2*aoa²
        '''

        self.cd0 = cd0
        self.d1 = d1
        self.d2 = d2

    def setAfilamento(self, gamma):
        '''
        Definindo o parametro de afilamento
        '''

        self.gamma = gamma


class Bemt:

    def __init__(self, rotor, correcao = False, elementosPa = 100):

        self.rotor = rotor
        self.correcao = correcao
        self.elementosPa = elementosPa

        rb = np.linspace(self.rotor.offset, 1, self.elementosPa, dtype=float)
        r_adim = [] 
        self.dr = float((rb[1]-rb[0]))
        for i in range(len(rb)-1):
            r_adim.append(rb[i]+self.dr/2)
        r_adim = np.array(r_adim, dtype=float)
        self.r_adim = r_adim
    
    # gradientes
    def _dCt_dr(self, solid, theta, rn, velInduzida):

        return 0.5*solid*self.rotor.cla*(theta*rn**2 - velInduzida*rn)

    def _dCq_dr(self, solid, theta, rn, velInduzida):
        ''' numericamente igual ao coef. de potencia '''

        return self._dCpi_dr(solid, theta, rn, velInduzida) + self._dCp0_dr(solid, theta, rn, velInduzida)

    def _dCpi_dr(self, solid, theta, rn, velInduzida):
        
        return 0.5*solid*self.rotor.cla*(theta*rn-velInduzida)*velInduzida*rn

    def _dCp0_dr(self, solid, theta, rn, velInduzida):
        
        return 0.5*solid*self._Cd(theta, velInduzida, rn)*rn**3

    def _Cd(self,theta, velInduzida, rn):
        phi = velInduzida/rn
        aoa = (theta - phi)
      
        return self.rotor.cd0+self.rotor.d1*aoa+self.rotor.d2*aoa**2

    def _coefSus(self, theta, rn, velInduzida):
        phi = velInduzida/rn
        return self.rotor.cla*(theta - phi)

    def _lambda_i(self, F, solid, theta, rn):

        return solid*self.rotor.cla/(16.0*F)*( np.sqrt( 1.0+32.0*F*theta*rn/(solid*self.rotor.cla) ) - 1.0)

    # correção de prandlt - para efeitos 3d
    def _f(self, rn, velInduzida):

        phi = velInduzida/rn

        return (self.rotor.numberBlades/2)*(1-rn)/(rn*phi)

    def _funPradtl(self, rn, velInduzida):

        return (2.0/np.pi)*np.arccos(np.exp(-self._f(rn,velInduzida)))

    def _solidLocal(self, rn):
        '''  Distribuicao de solidez ponderada pela tracao '''

        return ( (1-self.rotor.gamma)*rn + self.rotor.gamma )*self.rotor.solidEqui/( (1-self.rotor.gamma)*0.75 + self.rotor.gamma )

    def _BEMT(self, ctreq, twist):

        ''' Obtem a convergencia da velocidade induzida e angulo de torção inicial '''

        velInd = []
        Converge = True
        # theta em k = 0
        
        theta_0 = 6.0*ctreq/(self.rotor.solidEqui*self.rotor.cla) - 3.0*twist/4.0 + 3.0*np.sqrt(2*ctreq)/4.0
        
        i = 0

        while (i<10):

            Ct = 0.0

            if len(velInd) > 0:
                velInd.clear()

            
            for R_elem in self.r_adim:
                #print(f'{R_elem}')
                theta = theta_0 + R_elem*twist

                if( theta<0 ): 
                    Converge = False
                    break

                # definindo a solidez local 
                solid = self._solidLocal( R_elem )

                if (self.correcao == False):
                    vel = self._lambda_i(F = 1, solid = solid, theta = theta, rn = R_elem)
                
                if (self.correcao == True):

                    F = 1
                    vel = 0
                    swap = 10.e9

                    while( True ):
                        
                        vel = self._lambda_i( F, solid, theta, R_elem )
                        F = self._funPradtl( R_elem, vel )
                    

                        if ( abs(swap - vel) < 0.05 ):
                            break

                        swap = vel
                        
                velInd.append(vel)
                #print((solid,cla,theta,R_elem,dr,vel))
                Ct += self._dCt_dr( solid, theta, R_elem, vel )*self.dr 

            # theta em k+1

            dtheta = 6.0*(ctreq - Ct)/(self.rotor.solidEqui*self.rotor.cla) + (3.0*np.sqrt(2.0)/4)*( np.sqrt(ctreq) - np.sqrt(Ct) )
            
            i+=1
            if abs(dtheta) < 0.05 and Converge == False:
                break
        
            theta_0 = theta_0 + dtheta

        return Converge, theta_0, velInd

    def solver(self):
        
        
        k      = np.zeros( (len(self.rotor.ctreq) ))
        cp     = np.zeros( (len(self.rotor.ctreq) ))
        Fmerit = np.zeros( (len(self.rotor.ctreq) ))
        vel_ind= np.zeros( (len(self.rotor.ctreq), len(self.r_adim)) ) #linha, coluna

        for i in range(len(self.rotor.ctreq)):

            
            
            Converge, theta_0, vel_induzida = self._BEMT( self.rotor.ctreq[i], self.rotor.twist)
            vel_ind[i][:] = vel_induzida 

            if(Converge == False):
                print(f'Não para converge: ct = {self.rotor.ctreq[i]}, theta_disp = {self.rotor.twist*180/np.pi}')
                break

            # calculo dos parametros de desempenho 
            
            dct_dr = []
            dcq_dr = []
            cl     = []
            dcp    = [] # diferencial do coeficiente de potencia total
            dcpi   = [] # diferencial do coeficiente de potencia induzida
            dcp0   = [] # diferencial do coeficiente de potencia de perfil
        

            for index, rn in enumerate(self.r_adim):

                
                solid = self._solidLocal(rn)
                theta = theta_0 + rn*self.rotor.twist

                
                dcp0.append(self._dCp0_dr( solid, theta, rn, vel_induzida[index])*self.dr)

                # calculo dos gradientes
                dct_dr.append(self._dCt_dr(solid, theta, rn, vel_induzida[index]))
                dcq_dr.append(self._dCq_dr(solid, theta, rn, vel_induzida[index]))

                # difenrenciais
                dcp.append( self._dCq_dr(solid, theta, rn, vel_induzida[index])*self.dr)
                dcpi.append(self._dCpi_dr(solid, theta, rn, vel_induzida[index])*self.dr)

                # coeficientes
                cl.append( self._coefSus( theta, rn, vel_induzida[index] ) )

            # coeficiente de potencia/torque

            #print(theta_dis[j],sum(dcpi_dr))
            cp[i] = sum(dcp)
            cpi      = sum(dcpi)
            cp0      = sum(dcp0)
            # k = cpinduzida(considerando efeitos 3d)/ cpideal
            k[i]      = cpi/(self.rotor.ctreq[i]**(3/2)/np.sqrt(2))
            Fmerit[i] = (self.rotor.ctreq[i]**(3/2)/np.sqrt(2))/(k[i]*(self.rotor.ctreq[i]**(3/2)/np.sqrt(2))+cp0) 
            
    
        return dct_dr, dcq_dr, vel_ind, cl, k, cp, Fmerit    
        #obter a figura de merito e fator de pDotencia induzida




if __name__ == "__main__":
    theta_dis = [-10]
    Ctreq = [0.008]#np.linspace(0.002,0.009,10)
    rotorTeste = Rotor(cla = 5.9, ctreq = Ctreq, solidEqui = 0.1, numberBlades = 2, twist = theta_dis )
    rotorTeste.setArrato(cd0 = 0.01, d1 = 0.025 , d2 = 0.65)

    simula = Bemt( rotorTeste, correcao = True)
    __, __, __, cl1, k1, cp1, Fmerit1 = simula.solver()

    rotorTeste.setAfilamento(gamma = 2)
    simula = Bemt( rotorTeste, correcao = True)
    __, __, __, cl2, k2, cp2, Fmerit2 = simula.solver()

    rotorTeste.setAfilamento(gamma = 3)
    simula = Bemt( rotorTeste, correcao = True)
    __, __, __, cl3, k3, cp3, Fmerit3 = simula.solver()
   

    offset = 0.1
    npontos = 100 
    rb = np.linspace(offset, 1, npontos, dtype=float)
    radim = [] 
    dr = float((rb[1]-rb[0]))
    for i in range(len(rb)-1):
        radim.append(rb[i]+dr/2)
    radim = np.array(radim, dtype=float)

    plt.figure('Coeficiente de sustentação')
    plt.plot(simula.r_adim, cl1, label = r'$\gamma$ = 1')
    plt.plot(simula.r_adim, cl2, label = r'$\gamma$ = 2')
    plt.plot(simula.r_adim, cl3, label = r'$\gamma$ = 3')
    plt.xlabel('Raio adimensional')
    plt.ylabel(r'$C_l$')
    plt.legend()
    plt.grid()
    