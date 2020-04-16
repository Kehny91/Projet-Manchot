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
    masseTotal            = 0.3           #kg
    inertieTotal          = 0.1           #kg.m2, au centre de gravite par rapport a l axe Y
    
    #parametre aile droite
    ailesD_x_Foyer      = 0.01          #m, coordonnee x entre le centre de gravite et le foyer de l'aile
    ailesD_z_Foyer      = 0.01          #m, coordonnee z entre le centre de gravite et le foyer de l'aile
    aileD_S             = 0.2           #m2, surface ailaire
    aileD_Alpha_0       = 1*TORAD       #Radians
    aileD_CzA           = 1             #SI, dCz/dAlpha
    aileD_Cx0           = 1             #SI, trainee a portance nulle
    aileD_Allongemet    = 25            #SI, allongement = envergure**2/SurfacePortante
    aileD_k =   1/(pi*aileD_Allongemet) #SI, 
    flapsDMaxAngle      = 45*TORAD      #Radians
    flapsDPourcentage   = 0.2           #%, pourcentage d influence du flap sur l incidence de l aile
    
    #parametre aile gauche
    ailesG_x_Foyer      = 0.01          #m, coordonnee x entre le centre de gravite et le foyer de l'aile
    ailesG_z_Foyer      = 0.01          #m, coordonnee z entre le centre de gravite et le foyer de l'aile
    aileG_S             = 0.2           #m2, surface ailaire
    aileG_Alpha_0       = 1*TORAD       #Radians
    aileG_CzA           = 1             #SI, dCz/dAlpha
    aileG_Cx0           = 1             #SI, trainee a portance nulle
    aileG_Allongemet    = 25            #SI, allongement = envergure**2/SurfacePortante
    aileG_k =   1/(pi*aileD_Allongemet) #SI, 
    flapsGMaxAngle      = 45*TORAD      #Radians
    flapsGPourcentage   = 0.2           #%, pourcentage d influence du flap sur l incidence de l aile
    
    #parametre empennage droit
    empennageD_x_Foyer  = 0.01          #m, coordonnee x entre le centre de gravite et le foyer de la gouverne
    empennageD_z_Foyer  = -0.1          #m, coordonnee z entre le centre de gravite et le foyer de la gouverne
    empennageD_S        = 0.2           #m2, surface ailaire
    empennageD_Alpha_0  = 1*TORAD       #Radians
    empennageD_CzA      = 1             #SI, dCz/dAlpha
    empennageD_Cx0      = 1             #SI, trainee a portance nulle
    empennageD_Allongement= 25          #SI, allongement = envergure**2/SurfacePortante
    empennageD_k =1/(pi*empennageD_Allongement) #SI, 
    elevDMaxAngle        = 20*TORAD     #Radians
    elevDMaxAnglePourcentage = 0.2      #%, pourcentage d'influence de la gouverne sur l incidence de l empennage
    
    
    #parametre empennage gauche
    empennageG_x_Foyer  = 0.01          #m, coordonnee x entre le centre de gravite et le foyer de la gouverne
    empennageG_z_Foyer  = -0.1          #m, coordonnee z entre le centre de gravite et le foyer de la gouverne
    empennageG_S        = 0.2           #m2, surface ailaire
    empennageG_Alpha_0  = 1*TORAD       #Radians
    empennageG_CzA      = 1             #SI, dCz/dAlpha
    empennageG_Cx0      = 1             #SI, trainee a portance nulle
    empennageG_Allongement= 25          #SI, allongement = envergure**2/SurfacePortante
    empennageG_k =1/(pi*empennageG_Allongement) #SI, 
    elevGMaxAngle        = 20*TORAD     #Radians
    elevGMaxAnglePourcentage = 0.2      #%, pourcentage d'influence de la gouverne sur l incidence de l empennage
    
    #parametre propulseur
    engine_x            = 0.05          #m, coordonne x entre le centre de gravite et le centre de poussee du propulseur
    engine_z            = 0.1             #m, coordonne z entre le centre de gravite et le centre de poussee du propulseur
    engineMaxThrust     = 200           #Newton

    #parametre auto-pilote
    maxAutoPilotSpeed   = 200*TOMpS     #m/s
    maxAutoPilotZSpeed  = 20*TOMpS      #m/s


class ParametresSimulation:
    scriptToLoad = Scripts.scriptTest.ScriptExemple

