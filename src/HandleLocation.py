## module for handling of RTT positioning measurements
import math
import custom_log as log
from positiong_algorithm import * 

def Extract_and_Save_NRPPa_measurements(List_Meas,method):
    List_Meas_extracted=[]
    log.logger_LocAlg.info(f'Number of measuremtns included in this Measuremtn Response: {len(List_Meas)}')
    match method:
        case 'nr-Multi-RTT':
            log.logger_LocAlg.info("Start handle RTT measurements")
            for i,meas in enumerate(List_Meas):
                log.logger_LocAlg.debug(f'Information RTT measurement number: {i}')
                log.logger_LocAlg.debug(meas['measurementResult'][0]['measuredResultsValue'][1]['rxTxTimeDiff'])
                List_Meas_extracted.append( extract_meas_NRPPa(meas['measurementResult'][0]['measuredResultsValue'][1]['rxTxTimeDiff']))
            log.logger_LocAlg.info(f'The RTT measurements are: {List_Meas_extracted}')
        case 'nr-UL-TDOA':
            log.logger_LocAlg.info("Start handle TDOA measurements")
            for i,meas in enumerate(List_Meas):
                log.logger_LocAlg.debug(f'Information UL-RTOA measurement number: {i}')
                log.logger_LocAlg.debug(meas['measurementResult'][0]['measuredResultsValue'][1]['uLRTOAmeas'])
                List_Meas_extracted.append( extract_meas_NRPPa(meas['measurementResult'][0]['measuredResultsValue'][1]['uLRTOAmeas']))
            log.logger_LocAlg.info(f'The UL-RTOA measurements are: {List_Meas_extracted}')

    return List_Meas_extracted


def handle_NRPPa_measurements(List_Meas,method):
    log.logger_LocAlg.info(f'Number of measuremtns: {len(List_Meas)}')

    match method:
        case 'nr-Multi-RTT':
            log.logger_LocAlg.info("Start handle RTT measurements and positioning algorithm")
            try:
                estimation_pos= RTT_positioning_algorithm(List_Meas)
            except Exception as e:
                log.logger_LocAlg.error(f'Error in RTT positioning algorithm with error: {e}')
                estimation_pos= {}

        case 'nr-UL-TDOA':
            log.logger_LocAlg.info("Start handle TDOA measurements and positioning algorithm")
            TOA_measurements = list()


            id_TOA_reference = 0
            TOA_reference=List_Meas[id_TOA_reference]
            for i,RTOA in enumerate(List_Meas):
                if i!= id_TOA_reference:
                    TOA_measurements.append(RTOA)
                    
                    
            log.logger_LocAlg.info(f'The TOA measurements are: {TOA_measurements}')
            try:
                estimation_pos= TDOA_positioning_algorithm(TOA_reference,id_TOA_reference,TOA_measurements)
            except Exception as e:
                log.logger_LocAlg.error(f'Error in TDOA positioning algorithm with error: {e}')
                estimation_pos= {}
    return   estimation_pos


def handle_TDOA_measurements(prs_id_reference,TDOA_List_Meas):

    TOA_measurements=[0] * (len(TDOA_List_Meas))
    log.logger_LocAlg.info('Start handle TDOA measurements')

    for id,meas in enumerate(TDOA_List_Meas):
        if meas['dl-PRS-ID-r16'] == prs_id_reference['dl-PRS-ID-r16']:
            TOA_reference = extract_meas_LPP(meas['nr-RSTD-r16'])
            id_TOA_reference=id
    log.logger_LocAlg.debug(f"Reference id: {id_TOA_reference} with TOA: {TOA_reference}")
    ind=1
    for meas in TDOA_List_Meas:
        log.logger_LocAlg.debug(f"Information TDOA measurement number {ind}")
        log.logger_LocAlg.debug(meas['nr-RSTD-r16'])
        TOA_measurements[ind-1] = extract_meas_LPP(meas['nr-RSTD-r16']) 
        ind=ind+1

    log.logger_LocAlg.info(f"The TOA measurements are: {TOA_measurements[1:]}")

    try:
        estimation_pos= TDOA_positioning_algorithm(TOA_reference,id_TOA_reference,TOA_measurements[1:])
    except Exception as e:
        log.logger_LocAlg.error(f'Error in TDOA positioning algorithm with error: {e}')
        estimation_pos = {}
    if estimation_pos=={}:
        log.logger_LocAlg.error("Error in TDOA positioning algorithm")
        return "error"
    return estimation_pos

def handle_RTT_measurements(RTT_List_Meas):
    
    RTT_measurements=[0] * len(RTT_List_Meas)

    log.logger_LocAlg.info("Start handle RTT measurements")
    for i,meas in enumerate(RTT_List_Meas):
        log.logger_LocAlg.debug(f'Information RTT measurement number: {i}')
        log.logger_LocAlg.debug(meas['nr-UE-RxTxTimeDiff-r16'])
        RTT_measurements[i] = extract_meas_LPP(meas['nr-UE-RxTxTimeDiff-r16'])     


    log.logger_LocAlg.info(f'The RTT measurements are: {RTT_measurements}')
    estimation_pos= RTT_positioning_algorithm(RTT_measurements)

    # call function algoritm
    return  estimation_pos

def extract_meas_LPP(meas):
    delta_fmax = 480000
    Nf= 4096
    Tc=1/(delta_fmax*Nf)

    match meas[0]:
        case 'k0-r16':
            factor=1
        case 'k1-r16':
            factor=2
        case 'k2-r16':
            factor=4         
        case 'k3-r16':
            factor=8
        case 'k4-r16':
            factor= 16
        case 'k5-r16':
            factor=32

    max_value= math.ceil(1970049/factor)
    if meas[1]== 0:
        value= -985025  
    elif meas[1]== max_value:
        value= 985025
    else:
        value= ((meas[1]*factor - (985024) )*2-factor)/2 # Tc  

    return value * Tc #sec

def extract_meas_NRPPa(meas):
    delta_fmax = 480000
    Nf= 4096
    Tc=1/(delta_fmax*Nf)

    match meas[0]:
        case 'k0':
            factor=1
        case 'k1':
            factor=2
        case 'k2':
            factor=4         
        case 'k3':
            factor=8
        case 'k4':
            factor= 16
        case 'k5':
            factor=32

    max_value= math.ceil(1970049/factor)
    if meas[1]== 0:
        value= -985025  
    elif meas[1]== max_value:
        value= 985025
    else:
        value= ((meas[1]*factor - (985024) )*2-factor)/2 # Tc  

    return value * Tc #sec
