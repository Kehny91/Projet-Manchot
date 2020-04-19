import time
from math import sin,pi
import matplotlib.pyplot as plt

TODEG = 180/pi
TORAD = pi/180

def flattenFichier(fichier):
    ligne = fichier.readline() #entete
    out = []
    N = len(ligne.split())
    for i in range(N):
        out.append([])
    ligne = fichier.readline()
    while ligne != "\n":
        listed = ligne.split()
        for i in range(N):
            out[i].append(float(listed[i]))
        ligne = fichier.readline() 

    return out



class Polaire:
    """ Alpha positif = portance"""
    def getCl(self, alpha, v):
        pass

    def getCd(self, alpha, v):
        pass

    def getCm(self, alpha, v):
        """ Au bord d'attaque !! """
        pass 

class PolaireTabulee(Polaire):
    """ Alpha positif = portance"""
    def __init__(self,fichierCL,fichierCD,fichierCM_BA):
        """Attention l'ordre doit etre: alpha 1m/s alpha 10m/s alpha 15m/s alpha 20m/s alpha 40m/s alpha 5m/s alpha 60m/s"""
        super(PolaireTabulee,self).__init__()
        
        self._fichierCL = open(fichierCL,"r")
        self._fichierCD = open(fichierCD,"r")
        self._fichierCM_BA = open(fichierCM_BA,"r")

        self._flatCL = flattenFichier(self._fichierCL)
        self._flatCD = flattenFichier(self._fichierCD)
        self._flatCM = flattenFichier(self._fichierCM_BA)
    
    def _getAlphaAndValues(self, clcdcm, v):
        if clcdcm == "CL":
            use = self._flatCL
        elif clcdcm == "CD":
            use = self._flatCD
        elif clcdcm == "CM":
            use = self._flatCM
        else:
            assert False, "Pas un bon code"

        if v==1:
            indexAlpha = 0
        elif v==10:
            indexAlpha = 2
        elif v==15:
            indexAlpha = 4
        elif v==20:
            indexAlpha = 6
        elif v==40:
            indexAlpha = 8
        elif v==5:
            indexAlpha = 10
        elif v==60:
            indexAlpha = 12
        else:
            assert False, "Pas un bon code"

        return (use[indexAlpha],use[indexAlpha+1])

    def _round(self,v):
        if (v<=1):
            return 1
        elif (v<=5):
            return 5
        elif (v<=10):
            return 10
        elif (v<=15):
            return 15
        elif (v<=20):
            return 20
        elif (v<=40):
            return 40
        else:
            return 60

    def getCl(self, alpha, v):
        alpha = alpha*TODEG
        v = self._round(v)
        (alphas,values) = self._getAlphaAndValues("CL",v)
        i = 0
        n = len(alphas) 
        while (i<n-1 and alpha > alphas[i]):
            i+=1

        if (i == 0 or i == n-1): #DECROCHAGE
            #return 1.0 * sin(2*alpha*TORAD)
            return values[i]
        else:
            t = (alphas[i] - alpha)/(alphas[i]-alphas[i-1])
            return values[i]*(1-t) + values[i-1]*t

    def getCd(self, alpha, v):
        alpha = alpha*TODEG
        v = self._round(v)
        (alphas,values) = self._getAlphaAndValues("CD",v)
        i = 0
        n = len(alphas) 
        while (i<n-1 and alpha > alphas[i]):
            i+=1
        if (i == 0 or i == n-1): #DECROCHAGE
            #return 2.0 * abs(sin(alpha*TORAD))
            return values[i]
        else:
            t = (alphas[i] - alpha)/(alphas[i]-alphas[i-1])
            return values[i]*(1-t) + values[i-1]*t

    def getCm(self, alpha, v):
        alpha = alpha*TODEG
        v = self._round(v)
        (alphas,values) = self._getAlphaAndValues("CM",v)
        i = 0
        n = len(alphas) 
        while (i<n-1 and alpha > alphas[i]):
            i+=1
        if (i == 0 or i == n-1):
            return -1 * values[i] #SENS HORAIRE
        else:
            t = (alphas[i] - alpha)/(alphas[i]-alphas[i-1])
            return -1 * (values[i]*(1-t) + values[i-1]*t) #SENS HORAIRE
        
class PolaireLineaire(Polaire):
    """ Alpha positif = portance"""
    def __init__(self, Cza, a0, Cd0, k, Cm0):
        self._Cza = Cza
        self._a0 = a0
        self._Cd0 = Cd0
        self._k = k
        self._Cm0 = Cm0
    
    def getCl(self, alpha, v):
        if (abs(alpha)<20*TORAD):
            return self._Cza*sin(alpha + self._a0)
        else: #DECROCHAGE:
            return 1.0 * sin(2*alpha)
            #if (alpha>0):
            #    return self._Cza*sin(20*TORAD + self._a0)
            #else:
            #    return self._Cza*sin(-20*TORAD + self._a0)

    def getCd(self, alpha, v):
        if (abs(alpha)<20*TORAD):
            Cl = self.getCl(alpha, v)
            return self._Cd0 + (Cl**2)*self._k
        else:
            return 2.0 * abs(sin(alpha))

    def getCm(self, alpha, v):
        if (abs(alpha)<20*TORAD):
            return self._Cm0 + 0.25*self.getCl(alpha,v)
        else:
            if (alpha>0):
                return self._Cm0 + 0.25*self.getCl(20*TORAD,v)
            else:
                return self._Cm0 + 0.25*self.getCl(-20*TORAD,v)



        
        


if __name__ =="__main__":
    from Parametres import ParametresModele as PM
    c = PolaireTabulee("./XFLR5/CLwing","./XFLR5/CDwing","./XFLR5/CMwingBA")
    #c=PolaireLineaire(PM.empennageD_CzA, PM.empennageD_Alpha_0,PM.empennageD_Cx0, PM.empennageD_k,0)

    alphas = [-pi/2 + (i/1000)*(pi*3/2) for i in range(1000)]
    Cl = [c.getCl(a,676) for a in alphas]
    Cd = [c.getCd(a,676) for a in alphas]
    Cm = [c.getCm(a,676) for a in alphas]

    plt.plot(alphas,Cl)
    plt.plot(alphas,Cd)
    plt.plot(alphas,Cm)
    plt.show()