import Physique.Espace as E
import Physique.Solide as S
import Data.DataTypes as D

origine = E.Vecteur(-30,2.5,S.refSol)
scale = 0.3
spaceBetweenLetter = E.Vecteur(2*scale, 0, S.refSol)

class A:

    AC1_BG = E.Vecteur(0,0,S.refSol) + origine
    AC1_HD = E.Vecteur( 1*scale, 4*scale,S.refSol) + origine

    AC1 =  D.Obstacle(AC1_BG,AC1_HD,S.refSol)

    AC2_BG = AC1_HD
    AC2_HD = E.Vecteur(2*scale, 1*scale) + AC2_BG 

    AC2 = D.Obstacle(AC2_BG,AC2_HD,S.refSol)

    AC3_BG = E.Vecteur(AC1_HD.x,AC1_HD.z - 2*scale,S.refSol)
    AC3_HD = E.Vecteur(2*scale, 1*scale,S.refSol) + AC3_BG

    AC3 = D.Obstacle(AC3_BG,AC3_HD,S.refSol)

    AC4_BG = E.Vecteur(3*scale,0,S.refSol) + AC1_BG
    AC4_HD = E.Vecteur( 1*scale, 4*scale,S.refSol) + AC4_BG

    AC4 = D.Obstacle(AC4_BG,AC4_HD,S.refSol)

    LongeurA = E.Vecteur(4*scale,0,S.refSol)

class L:
    LC1_BG = E.Vecteur(0,0,S.refSol) + origine + A.LongeurA + spaceBetweenLetter
    LC1_HD = E.Vecteur(1*scale, 5*scale, S.refSol) + LC1_BG

    LC1 = D.Obstacle(LC1_BG, LC1_HD, S.refSol)

    LC2_BG = E.Vecteur(1*scale,0,S.refSol) + LC1_BG
    LC2_HD = E.Vecteur(3*scale,1*scale,S.refSol) + LC2_BG

    LC2 = D.Obstacle(LC2_BG, LC2_HD, S.refSol)

    LongeurL = E.Vecteur(4*scale,0,S.refSol)

class Eprime:
    EC1_BG = E.Vecteur(0,0,S.refSol) + origine + A.LongeurA + L.LongeurL + spaceBetweenLetter*2
    EC1_HD = E.Vecteur(1*scale, 5*scale, S.refSol) + EC1_BG

    EC1 = D.Obstacle(EC1_BG, EC1_HD, S.refSol)

    EC2_BG = EC1_HD
    EC2_HD = E.Vecteur(2*scale, -1*scale,S.refSol) + EC2_BG

    EC2 = D.Obstacle(EC2_BG, EC2_HD, S.refSol)

    EC3_BG = EC1_BG
    EC3_HD = E.Vecteur(3*scale, 1*scale,S.refSol) + EC1_BG

    EC3 = D.Obstacle(EC3_BG, EC3_HD, S.refSol)

    EC4_BG = E.Vecteur(EC1_HD.x,EC1_HD.z - (3*scale),S.refSol)
    EC4_HD = E.Vecteur(1*scale, 1*scale,S.refSol) + EC4_BG

    EC4 = D.Obstacle(EC4_BG, EC4_HD, S.refSol)

    LongeurE = E.Vecteur(3*scale,0,S.refSol)

class X:

    XC1_BG = E.Vecteur(0,0,S.refSol) + origine + A.LongeurA + L.LongeurL + Eprime.LongeurE + spaceBetweenLetter*3
    XC1_HD = E.Vecteur(1*scale, 2*scale, S.refSol) + XC1_BG

    XC1 = D.Obstacle(XC1_BG, XC1_HD, S.refSol)

    XC2_BG = E.Vecteur(0,3*scale,S.refSol) + XC1_BG
    XC2_HD = E.Vecteur(1*scale, 2*scale, S.refSol) + XC2_BG

    XC2 = D.Obstacle(XC2_BG, XC2_HD, S.refSol)

    XC3_BG = E.Vecteur(1*scale,2*scale,S.refSol) + XC1_BG
    XC3_HD = E.Vecteur(1*scale, 1*scale,S.refSol) + XC3_BG

    XC3 = D.Obstacle(XC3_BG, XC3_HD, S.refSol)

    XC4_BG = E.Vecteur(2*scale,0,S.refSol) + XC1_BG
    XC4_HD = E.Vecteur(1*scale, 2*scale,S.refSol) + XC4_BG

    XC4 = D.Obstacle(XC4_BG, XC4_HD, S.refSol)

    XC5_BG = E.Vecteur(2*scale,3*scale,S.refSol) + XC1_BG
    XC5_HD = E.Vecteur(1*scale, 3.5-3*scale,S.refSol) + XC5_BG

    XC5 = D.Obstacle(XC5_BG, XC5_HD, S.refSol)

    LongeurX = E.Vecteur(3*scale,0,S.refSol)
    OrigineX = XC1_BG + LongeurX 

class Esp:
    EspC1_BG = X.OrigineX + spaceBetweenLetter*2
    EspC1_HD = E.Vecteur(2*scale, 1*scale, S.refSol) + EspC1_BG

    EspC1 = D.Obstacle(EspC1_BG, EspC1_HD, S.refSol)

    EspC2_BG = E.Vecteur(0,2*scale,S.refSol) + EspC1_BG
    EspC2_HD = E.Vecteur(1*scale, 2*scale, S.refSol) + EspC2_BG

    EspC2 = D.Obstacle(EspC2_BG, EspC2_HD, S.refSol)

    EspC3_BG = E.Vecteur(1*scale,4*scale,S.refSol) + EspC1_BG
    EspC3_HD = E.Vecteur(2*scale, 1*scale, S.refSol) + EspC3_BG

    EspC3 = D.Obstacle(EspC3_BG, EspC3_HD, S.refSol)

    LongeurEsp = E.Vecteur(3*scale,0,S.refSol)
    OrigineEsp = EspC1_BG + LongeurEsp

class T:
    TC1_BG = E.Vecteur(0,4*scale,S.refSol) + Esp.OrigineEsp + spaceBetweenLetter*2
    TC1_HD = E.Vecteur(5*scale, 1*scale, S.refSol) + TC1_BG

    TC1 = D.Obstacle(TC1_BG, TC1_HD, S.refSol)

    TC2_BG = E.Vecteur(2*scale,0,S.refSol) + Esp.OrigineEsp + spaceBetweenLetter*2
    TC2_HD = E.Vecteur(1*scale, 4*scale, S.refSol) + TC2_BG

    TC2 = D.Obstacle(TC2_BG, TC2_HD, S.refSol)

    LongeurT = E.Vecteur(5*scale,0,S.refSol)
    OrigineT = Esp.OrigineEsp + spaceBetweenLetter*2 + LongeurT

class O:

    OC1_BG = E.Vecteur(0,1*scale,S.refSol) + T.OrigineT + spaceBetweenLetter
    OC1_HD = E.Vecteur(1*scale, 3*scale, S.refSol) + OC1_BG

    OC1 = D.Obstacle(OC1_BG, OC1_HD, S.refSol)

    OC2_BG = E.Vecteur(1*scale,0,S.refSol) + T.OrigineT + spaceBetweenLetter
    OC2_HD = E.Vecteur(2*scale, 1*scale, S.refSol) + OC2_BG

    OC2 = D.Obstacle(OC2_BG, OC2_HD, S.refSol)

    OC3_BG = OC2_HD
    OC3_HD = E.Vecteur(1*scale, 3*scale, S.refSol) + OC3_BG

    OC3 = D.Obstacle(OC3_BG, OC3_HD, S.refSol)

    OC4_BG = OC1_HD
    OC4_HD = E.Vecteur(2*scale, 1*scale, S.refSol) + OC4_BG

    OC4 = D.Obstacle(OC4_BG, OC4_HD, S.refSol)

    LongeurO = E.Vecteur(4*scale,0,S.refSol)
    OrigineO = T.OrigineT + spaceBetweenLetter + LongeurO

class M:
    MC1_BG =  O.OrigineO + spaceBetweenLetter
    MC1_HD = E.Vecteur(1*scale, 5*scale, S.refSol) + MC1_BG

    MC1 = D.Obstacle(MC1_BG, MC1_HD, S.refSol)

    MC2_BG = MC1_HD
    MC2_HD = E.Vecteur(1*scale, -1*scale, S.refSol) + MC2_BG

    MC2 = D.Obstacle(MC2_BG, MC2_HD, S.refSol)

    MC3_BG =  MC2_HD
    MC3_HD = E.Vecteur(1*scale, -1*scale, S.refSol) + MC3_BG

    MC3 = D.Obstacle(MC3_BG, MC3_HD, S.refSol)

    MC4_BG = E.Vecteur(0, 1*scale, S.refSol) + MC3_HD
    MC4_HD = E.Vecteur(1*scale, 1*scale, S.refSol) + MC4_BG

    MC4 = D.Obstacle(MC4_BG, MC4_HD, S.refSol)

    MC5_BG = MC4_HD
    MC5_HD = E.Vecteur(1*scale, -5*scale, S.refSol) + MC5_BG

    MC5 = D.Obstacle(MC5_BG, MC5_HD, S.refSol)

    LongeurM = E.Vecteur(5*scale,0,S.refSol)
    OrigineM = O.OrigineO + spaceBetweenLetter + LongeurM


class Ob1:
    ob1 = D.Obstacle(E.Vecteur(M.OrigineM.x-1*scale,0, S.refSol),E.Vecteur(M.OrigineM.x,2.5, S.refSol), S.refSol)

class Ob2 : 
    ob2 = D.Obstacle(E.Vecteur(X.OrigineX.x-1*scale,6, S.refSol),E.Vecteur(0,6.2, S.refSol), S.refSol)

class Ob3 : 
    ob3 = D.Obstacle(E.Vecteur(-3.5,6, S.refSol),E.Vecteur(-4.3,0.6, S.refSol), S.refSol)

class Ob4:
    ob4 = D.Obstacle(E.Vecteur(-0.2,0, S.refSol),E.Vecteur(0,0.8, S.refSol), S.refSol)

class Ob5:
    ob5 = D.Obstacle(E.Vecteur(-0.2,0.8, S.refSol),E.Vecteur(30,1, S.refSol), S.refSol)
