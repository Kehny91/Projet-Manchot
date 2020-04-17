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
    def __init__(self,fichierCL,fichierCD,fichierCM_BA):
        """Attention l'ordre doit etre: alpha 1m/s alpha 10m/s alpha 15m/s alpha 20m/s alpha 40m/s alpha 5m/s alpha 60m/s"""
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
            return 1.0 * sin(2*alpha*TORAD)
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
            return 2.0 * abs(sin(alpha*TORAD))
        else:
            t = (alphas[i] - alpha)/(alphas[i]-alphas[i-1])
            return values[i]*(1-t) + values[i-1]*t

    def getCM(self, alpha, v):
        alpha = alpha*TODEG
        v = self._round(v)
        (alphas,values) = self._getAlphaAndValues("CM",v)
        i = 0
        n = len(alphas) 
        while (i<n-1 and alpha > alphas[i]):
            i+=1
        if (i == 0 or i == n-1):
            return values[i]
        else:
            t = (alphas[i] - alpha)/(alphas[i]-alphas[i-1])
            return values[i]*(1-t) + values[i-1]*t
        



        
        


if __name__ =="__main__":
    c = Polaire("./XFLR5/CLwing","./XFLR5/CDwing","./XFLR5/CMwingBA")

    alphas = [-pi/2 + (i/1000)*(pi) for i in range(1000)]
    Cl = [c.getCl(a,676) for a in alphas]
    Cd = [c.getCd(a,676) for a in alphas]
    Cm = [c.getCM(a,676) for a in alphas]

    plt.plot(alphas,Cl)
    plt.plot(alphas,Cd)
    plt.plot(alphas,Cm)
    plt.show()