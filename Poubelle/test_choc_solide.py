
from math import cos,sin,pi,sqrt,atan2
import pygame as pg
import pygame.draw as draw
import pygame.font as font
import pygame.color as color
import pygame.surface as surface
import time

frottementFluide = 0.1

class Solide:
    def __init__(self, x=0, z=0, theta=0, mass=0, vx=0, vz=0, w=0):
        self.x = x
        self.z = z
        self.vx = vx
        self.vz = vz
        self.w = w
        self.theta = theta
        self.attachements=[]
        self.mass = mass
        self.I = self.mass*((0.1**2)+(0.2**2))/12

    def addAttachement(self, attachement):
        self.attachements.append(attachement)
        attachement.father = self

    def updateCinetique(self, dt):
        (fx,fz,m) = self.computeTorseur()
        accX = fx/self.mass
        accZ = fz/self.mass
        wpoint = m/self.I
        self.vx += accX*dt
        self.vz += accZ*dt
        self.w += wpoint*dt
        self.theta += self.w*dt
        self.x += self.vx*dt
        self.z += self.vz*dt

    def computeTorseur(self):
        out = [-self.vx*frottementFluide,-self.vz*frottementFluide - self.mass*9.81,0] #x,z,moment
        for p in self.attachements:
            thisForce = p.getForce()
            out[0] += thisForce[0]
            out[1] += thisForce[1]
            out[2] += p.getCurrentDx()*thisForce[1] - p.getCurrentDz()*thisForce[0]
        return out


class Attachements:
    def __init__(self, dx, dz):
        self.father = Solide()
        self.dx = dx
        self.dz = dz

    def getX(self):
        return self.father.x + cos(self.father.theta)*self.dx - sin(self.father.theta)*self.dz

    def getZ(self):
        return self.father.z + cos(self.father.theta)*self.dz + sin(self.father.theta)*self.dx

    def getCurrentDx(self):
        return self.getX() - self.father.x

    def getCurrentDz(self):
        return self.getZ() - self.father.z

    def getVz(self):
        currentDx = self.getX() - self.father.x
        return self.father.vz + self.father.w*currentDx

    def getVx(self):
        currentDz = self.getZ() - self.father.z
        return self.father.vx - self.father.w*currentDz

    def toucheLeSol(self):
        return self.getZ()<=0

    def getForce(self):
        return (0,0)

class PointContact(Attachements):
    def __init__(self,dx,dz,k,r):
        super().__init__(dx,dz)
        self.k = k
        self.r = r

    def getForce(self):
        if self.toucheLeSol():
            fn = -1*self.k*self.getZ() -1*self.r*self.getVz()

            return (0,fn)
        else:
            return (0,0)



pixWIDTH = 900
pixHEIGHT = 900
scale = 0.0065 #m/pix (combien de m en 1 pixel)


def realToPix(posReal):
    (realX,realZ) = posReal
    return (int(realX//scale + pixWIDTH//2) , int(pixHEIGHT - realZ//scale))

K=5000
R = 20

if __name__ == "__main__":
    casserolle = Solide(0,4,0,1,1,0,3.14)
    casserolle.addAttachement(PointContact(0.1,0.05,K,R))
    casserolle.addAttachement(PointContact(0.1,-0.05,K,R))
    casserolle.addAttachement(PointContact(-0.1,0.049,K,R))
    casserolle.addAttachement(PointContact(-0.1,-0.05,K,R))
    casserolle.addAttachement(PointContact(-0.3,0.05,K,R))
    pg.init()
    font.init()
    screen = pg.display.set_mode((pixWIDTH,pixHEIGHT))
    dt = 1/60

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    myFont = font.Font(None,100)
    t = 0
    for i in range (int(10/dt)):
        tStart = time.time()
        casserolle.updateCinetique(dt)
        t +=dt
        textSurface = myFont.render(str(t),True,color.Color(255,0,0,0))
        screen.blit(background,(0,0))
        screen.blit(textSurface,(0,0))
        for point in casserolle.attachements:
            if point.toucheLeSol():
                draw.circle(screen,pg.color.Color(255,0,0,0),realToPix((point.getX(),point.getZ())),7)
            else:
                draw.circle(screen,pg.color.Color(0,255,0,0),realToPix((point.getX(),point.getZ())),7)
        pg.display.flip()
        time.sleep(max(0,dt-(time.time()-tStart)))