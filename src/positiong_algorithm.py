import numpy as np
from datetime import datetime, timezone
import time
import custom_log as log
import math
import config



def TDOA_positioning_algorithm(TOA_reference,id_TOA_reference,TOA_measurements):
    log.logger_LocAlg.info("Positioning algorithm: TDOA")
    speedofLigth = 299792458


    gNBPos_config= config.gNBPos
    D1=TOA_reference*speedofLigth
    XR2, YR2,D2 = [], [], []
    XR1= gNBPos_config[id_TOA_reference][0]
    YR1= gNBPos_config[id_TOA_reference][1]
    for pos,i in gNBPos_config:
        if i!=id_TOA_reference:
            XR2.append(pos['x'])
            YR2.append(pos['y'])
            D2.append(TOA_measurements)

    try:
        [x,y] = LS_TDOA(XR1,YR1,D1, XR2, YR2, D2)
    except Exception as e:
        log.logger_LocAlg.error(f'Error in RTT positioning algorithm with error: {e}')
        return {}

    current_datetime = datetime.now(timezone.utc)
    formatted_timestamp = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")   
    try:
        lat, lon= cartesian_to_gps(result[0], result[1], 0)
    except Exception as e:
        log.logger_LocAlg.error(f'Error in converting cartesian to gps with error: {e}')
        return {}
    result = { 'locationEstimate': {
                            'shape': 'POINT',
                            'point': {
                                        'lat': lat, 
                                        'lon': lon
                                        }
                            }, 
             'timestampOfLocationEstimate': formatted_timestamp
             }
    
    log.logger_LocAlg.info(f"Result of the estimation: {result}")

    return result

def RTT_positioning_algorithm(value):
    log.logger_LocAlg.info("Positioning algorithm: RTT")
    speedofLigth = 299792458

    rtt_dist=[i * speedofLigth for i in value]
    log.logger_LocAlg.debug(f"INPUT are: rtt_dist: {rtt_dist}")
    gNBPos= config.gNBPos
    
    XR2, YR2 = [], []

    for pos in gNBPos:
        XR2.append(pos['x'])
        YR2.append(pos['y'])

    try:
        [x,y] = LS_RTT(XR2,YR2,rtt_dist)
    except Exception as e:
        log.logger_LocAlg.error(f'Error in RTT positioning algorithm with error: {e}')
        return {}
    
    current_datetime = datetime.now(timezone.utc)
    formatted_timestamp = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")    
    try:
        lat, lon= cartesian_to_gps(x, y, 0)
    except Exception as e:
        log.logger_LocAlg.error(f'Error in converting cartesian to gps with error: {e}')
        return {}
    result = { 'locationEstimate': {
                            'shape': 'POINT',
                            'point': {
                                        'lat': lat, 
                                        'lon': lon
                                        }
                            }, 
             'timestampOfLocationEstimate': formatted_timestamp
             }
    log.logger_LocAlg.info(f"Result of the estimation: {result}")
    return result


# LEAST SQUARE ALGORITHM BASED ON RTT   
def LS_RTT(XR2, YR2, D2):

    GX, GY = np.meshgrid(np.arange(100, 301, 0.1), np.arange(100, 301, 0.1))
    GPz = np.column_stack((GX.flatten(), GY.flatten()))


    res = []
    res= np.empty((len(GPz),len(XR2)))
    for ii in range(len(XR2)):
        d2 = np.sqrt((XR2[ii] - GPz[:, 0]) ** 2 + (YR2[ii] - GPz[:, 1]) ** 2)
        res[:,ii]= ((d2 - D2[ii]) ** 2)

    res = np.array(res)
    i = np.argmin(np.sum(res, axis=1))
    x = GPz[i]
    return x

# LEAST SQUARE ALGORITHM BASED ON TDOA   
def LS_TDOA(XR1,YR1,D1, XR2, YR2, D2):

    GX, GY = np.meshgrid(np.arange(100, 301, 0.1), np.arange(100, 301, 0.1))
    GPz = np.column_stack((GX.flatten(), GY.flatten()))


    res = []
    res= np.empty((len(GPz),len(XR2)))
    for ii in range(len(XR2)):
        d1= np.sqrt( (XR1- GPz[:,0])**2 + (YR1-GPz[:,1])**2)
        d2 = np.sqrt((XR2[ii] - GPz[:, 0]) ** 2 + (YR2[ii] - GPz[:, 1]) ** 2)

        res[:,ii]= ((d1-d2) - (D1-D2[ii]))**2
        ((d2 - D2[ii]) ** 2)

    res = np.array(res)
    i = np.argmin(np.sum(res, axis=1))
    x = GPz[i]
    return x

def cartesian_to_gps(x, y, z):

    # origin lat and lon are the coordinates of the origin of the cartesian system (0,0,0)
    origin_lat = config.origin_lat 
    origin_lon = config.origin_lon

    earth_radius = 6378137.0 # Earth radius in meters
    lat = origin_lat + (x / earth_radius) * (180 / math.pi)
    lon = origin_lon + (y / earth_radius) * (180 / math.pi) / math.cos(origin_lat * math.pi / 180)
    return lat, lon
