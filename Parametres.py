from math import pi
import Modes
import Scripts.scriptTest
TORAD = pi/180
TODEG = 180/pi
TOMpS = 1/3.6

class ConstanteEnvironement:
    rho_air_0               = 1.225         #kg/m3, masse volumique de l air a une altitude nulle
    g_0                     = 9.81          #m.s-2, acceleration de pesenteur a altitude nulle

class ParametresModele:
    #parametre structure
    masseTotal              = 3             #kg
    inertieTotal            = 0.045         #kg.m2, au centre de gravite par rapport a l axe Y
    longueurDrone           = 1.1           #m
    
    #parametre aile droite
    ailesD_x_BA             = -0.15         #m, coordonnee x entre le centre de gravite et le bord d'attaque de l'aile
    ailesD_z_BA             = 0.062         #m, coordonnee z entre le centre de gravite et le bord d'attaque de l'aile
    ailesD_corde            = 0.2           #m
    aileD_S                 = 0.145         #m2, surface alaire
    aileD_Alpha_0           = -2.5*TORAD    #Radians
    flapsDMaxAngle          = 45*TORAD      #Radians
    flapsDPourcentageCordeArticulee = 0.5   #%
    flapsDPourcentageEnvergureArticulee = 0.5 #%
    
    #parametre aile gauche
    ailesG_x_BA             = -0.15         #m, coordonnee x entre le centre de gravite et le bord d'attaque de l'aile
    ailesG_z_BA             = 0.062         #m, coordonnee z entre le centre de gravite et le bord d'attaque de l'aile
    ailesG_corde            = 0.2           #m
    aileG_S                 = 0.145         #m2, surface alaire
    aileG_Alpha_0           = -2.5*TORAD    #Radians
    flapsGMaxAngle          = 45*TORAD      #Radians
    flapsGPourcentageCordeArticulee = 0.5 #%
    flapsGPourcentageEnvergureArticulee = 0.5 #%
    
    #parametre empennage droit
    empennageD_x_BA         = -1.02          #m, coordonnee x entre le centre de gravite et le BA du stab
    empennageD_z_BA         = 0.1            #m, coordonnee z entre le centre de gravite et le BA du stab
    empennageD_corde        = 0.115          #m
    empennageD_S            = 0.0485         #m2, surface ailaire
    empennageD_Alpha_0      = -2.5*TORAD     #Radians
    elevDMaxAngle           = 20*TORAD       #Radians
    elevDPourcentageCordeArticulee = 0.7     #%
    elevDPourcentageEnvergureArticulee = 1   #L'elevator a une gouverne sur toute son envergure !
    
    
    #parametre empennage gauche
    empennageG_x_BA         = -1.02          #m, coordonnee x entre le centre de gravite et le BA du stab
    empennageG_z_BA         = 0.1            #m, coordonnee z entre le centre de gravite et le BA du stab
    empennageG_corde        = 0.115          #m
    empennageG_S            =  0.0485        #m2, surface ailaire
    empennageG_Alpha_0      = -2.5*TORAD     #Radians
    elevGMaxAngle           = 20*TORAD      #Radians
    elevGPourcentageCordeArticulee = 0.7    #%
    elevGPourcentageEnvergureArticulee = 1  #L'elevator a une gouverne sur toute son envergure !
    
    #parametre propulseur
    engine_x                = 0.083          #m, coordonne x entre le centre de gravite et le centre de poussee du propulseur
    engine_z                = 0.01           #m, coordonne z entre le centre de gravite et le centre de poussee du propulseur
    engineMaxThrust         = 45             #Newton
    engineMaxPow            = 505            #Watt
    engine_tau              = 0.001            #s, temps de reaction du moteur

    #parametre auto-pilote
    maxAutoPilotSpeed       = 200*TOMpS      #m/s
    maxAutoPilotZSpeed      = 20*TOMpS       #m/s

    #parametres collision
    p1_x                    = 0.028 + engine_x         #m, coordonne x entre le centre de gravite et le corps rigide
    p1_z                    = 0 + engine_z             #m, coordonne z entre le centre de gravite et le corps rigide

    p2_x                    = 0.0086 + engine_x        #m, coordonne x entre le centre de gravite et le corps rigide               
    p2_z                    = 0.018 + engine_z         #m, coordonne z entre le centre de gravite et le corps rigide

    p3_x                    = -0.073 + engine_x        #m, coordonne x entre le centre de gravite et le corps rigide
    p3_z                    = -0.040 + engine_z        #m, coordonne z entre le centre de gravite et le corps rigide

    p4_x                    = -0.335 + engine_x        #m, coordonne x entre le centre de gravite et le corps rigide
    p4_z                    = -0.050 + engine_z        #m, coordonne z entre le centre de gravite et le corps rigide

    p5_x                    = -1.176+ engine_x        #m, coordonne x entre le centre de gravite et le corps rigide
    p5_z                    = -0.03 + engine_z        #m, coordonne z entre le centre de gravite et le corps rigide

    p6_x                    = -1.180 + engine_x        #m, coordonne x entre le centre de gravite et le corps rigide
    p6_z                    = -0.04 + engine_z         #m, coordonne z entre le centre de gravite et le corps rigide

    p7_x                    = -1.207 + engine_x        #m, coordonne x entre le centre de gravite et le corps rigide
    p7_z                    = -0.173 + engine_z         #m, coordonne z entre le centre de gravite et le corps rigide

    p8_x                    = -1.120 + engine_x         #m, coordonne x entre le centre de gravite et le corps rigide
    p8_z                    = -0.177 + engine_z         #m, coordonne z entre le centre de gravite et le corps rigide

    muFrottementSol         = 0.8                      #SI, coef de frottement avec le sol


class ParametresSimulation:
    scriptToLoad = Scripts.scriptTest.ScriptExemple             #Classe Script a utiliser
    maxAcceptablePenetrationSpeed = 0.001                       #m/s
    positionXPiste = 15                                         #m
    longueurXPiste = 15                                         #m

    positionXIni = 0                                            #m/s
    positionZIni = 20                                           #m/s
    assietteIni = 0                                             #m/s
    vitesseXIni = 10                                            #m/s
    vitesseZIni = 0                                             #m/s
    wIni = 0                                                    #m/s


    frequenceMixer = 50                                         #Hz
    frequenceAsservissement = 50                                #Hz
    frequenceAffichage = 40                                     #Hz
    frequencePhysique = 150                                     #Hz

    dilatation = 5                                              #secondeDeSimulation/secondeVraie  
                                                                #(ie si dilatation = 2, il faut 2 seconde pour qu'une seconde s'ecoule dans le simu)
                                                                #Le csv donne toujours le temps simu.

    scaleAffichage = 0.02                                       #m/pix

    logOnly = False                                             #Permet de desactiver l'interface graphique 
    modeInitial = Modes.MODE_AUTO_PILOT

    #DEBUG
    printForces = False

