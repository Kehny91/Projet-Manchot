from math import pi
import Scripts.scriptTest
TORAD = pi/180
TODEG = 180/pi
TOMpS = 1/3.6

class ConstanteEnvironement:
    rho_air_0           = 1.225         #kg/m3, masse volumique de l air a une altitude nulle
    g_0                 = 9.81          #m.s-2, acceleration de pesenteur a altitude nulle

class ParametresModele:
    #parametre structure
    masseTotal            = 10           #kg
    inertieTotal          = 0.045           #kg.m2, au centre de gravite par rapport a l axe Y
    
    #parametre aile droite
    #ailesD_x_Foyer      = 0.01          #m, coordonnee x entre le centre de gravite et le foyer de l'aile
    #ailesD_z_Foyer      = 0.01          #m, coordonnee z entre le centre de gravite et le foyer de l'aile
    ailesD_x_BA      = -0.2             #m, coordonnee x entre le centre de gravite et le bord d'attaque de l'aile
    ailesD_z_BA      = 0.01             #m, coordonnee z entre le centre de gravite et le bord d'attaque de l'aile
    ailesD_corde        = 0.2           #m
    aileD_S             = 0.25           #m2, surface alaire
    aileD_Alpha_0       = -2.5*TORAD    #Radians
    aileD_CzA           = 0.944*TORAD         #SI, dCz/dAlpha
    aileD_Cx0           = 0.00            #SI, trainee a portance nulle
    aileD_Allongemet    = 10000            #SI, allongement = envergure**2/SurfacePortante
    aileD_k             =   1/(pi*aileD_Allongemet) #SI, 
    flapsDMaxAngle      = 45*TORAD      #Radians
    flapsDPourcentage   = 0.5           #%, pourcentage d influence du flap sur l incidence de l aile
    
    #parametre aile gauche
    #ailesG_x_Foyer      = 0.01          #m, coordonnee x entre le centre de gravite et le foyer de l'aile
    #ailesG_z_Foyer      = 0.01          #m, coordonnee z entre le centre de gravite et le foyer de l'aile
    ailesG_x_BA      = -0.2             #m, coordonnee x entre le centre de gravite et le bord d'attaque de l'aile
    ailesG_z_BA      = 0.01             #m, coordonnee z entre le centre de gravite et le bord d'attaque de l'aile
    ailesG_corde        = 0.2           #m
    aileG_S             = 0.25           #m2, surface alaire
    aileG_Alpha_0       = -2.5*TORAD      #Radians
    aileG_CzA           = 0.944*TORAD             #SI, dCz/dAlpha
    aileG_Cx0           = 0.00             #SI, trainee a portance nulle
    aileG_Allongemet    = 10000            #SI, allongement = envergure**2/SurfacePortante
    aileG_k             =   1/(pi*aileD_Allongemet) #SI, 
    flapsGMaxAngle      = 45*TORAD      #Radians
    flapsGPourcentage   = 0.5           #%, pourcentage d influence du flap sur l incidence de l aile
    
    #parametre empennage droit
    #empennageD_x_Foyer  = 0.01          #m, coordonnee x entre le centre de gravite et le foyer de la gouverne
    #empennageD_z_Foyer  = -0.1          #m, coordonnee z entre le centre de gravite et le foyer de la gouverne
    empennageD_x_BA  = -1.5             #m, coordonnee x entre le centre de gravite et le BA du stab
    empennageD_z_BA  = -0.1             #m, coordonnee z entre le centre de gravite et le BA du stab
    empennageD_corde = 0.1              #m
    empennageD_S        = 0.1           #m2, surface ailaire
    empennageD_Alpha_0  = 0*TORAD       #Radians
    empennageD_CzA      = 10             #SI, dCz/dAlpha
    empennageD_Cx0      = 0             #SI, trainee a portance nulle
    empennageD_Allongement= 25          #SI, allongement = envergure**2/SurfacePortante
    empennageD_k =1/(pi*empennageD_Allongement) #SI, 
    elevDMaxAngle        = 20*TORAD     #Radians
    elevDPourcentage = 0.2      #%, pourcentage d'influence de la gouverne sur l incidence de l empennage
    
    
    #parametre empennage gauche
    #empennageG_x_Foyer  = 0.01          #m, coordonnee x entre le centre de gravite et le foyer de la gouverne
    #empennageG_z_Foyer  = -0.1          #m, coordonnee z entre le centre de gravite et le foyer de la gouverne
    empennageG_x_BA  = -1.5             #m, coordonnee x entre le centre de gravite et le BA du stab
    empennageG_z_BA  = -0.1             #m, coordonnee z entre le centre de gravite et le BA du stab
    empennageG_corde = 0.1              #m
    empennageG_S        = 0.1           #m2, surface ailaire
    empennageG_Alpha_0  = 0*TORAD       #Radians
    empennageG_CzA      = 10             #SI, dCz/dAlpha
    empennageG_Cx0      = 0             #SI, trainee a portance nulle
    empennageG_Allongement= 25          #SI, allongement = envergure**2/SurfacePortante
    empennageG_k =1/(pi*empennageG_Allongement) #SI, 
    elevGMaxAngle        = 20*TORAD     #Radians
    elevGPourcentage = 0.2      #%, pourcentage d'influence de la gouverne sur l incidence de l empennage
    
    #parametre propulseur
    engine_x            = .08          #m, coordonne x entre le centre de gravite et le centre de poussee du propulseur
    engine_z            =  0.01           #m, coordonne z entre le centre de gravite et le centre de poussee du propulseur
    engineMaxThrust     = 200           #Newton

    #parametre auto-pilote
    maxAutoPilotSpeed   = 200*TOMpS     #m/s
    maxAutoPilotZSpeed  = 20*TOMpS      #m/s


class ParametresSimulation:
    scriptToLoad = Scripts.scriptTest.ScriptExemple

