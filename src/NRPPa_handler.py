from pycrate_asn1dir import NRPPa
import NRPPa_message_gen as gen_nrppa
from NRPPa_message_gen import ProcedureCodeEP
from NRPPa_message_gen import IEs_id
import config
import copy
import custom_log as log
import lmf_instance as lmf
import HandleLocation as HandleLocation
from datetime import datetime, timezone
import time


def decodeNRPPa(NRPPa_message_ANS1):
    try:
        #decode the nrppa messagge from asn1
        log.logger_NRPPa.info(' Decoded the NRPPa message')
        M=NRPPa.NRPPA_PDU_Descriptions.NRPPA_PDU
        M.from_aper(NRPPa_message_ANS1)
        decoded_message_NRPPa = copy.deepcopy(M())
        return decoded_message_NRPPa
    except:
        log.logger_NRPPa.error('Error in decoding NRPPa message')
        return None

def encodeNRPPa(NRPPa_message):
    try:
        #encode the nrppa messagge from asn1
        log.logger_NRPPa.info(' Encoded the NRPPa message')
        M=NRPPa.NRPPA_PDU_Descriptions.NRPPA_PDU
        M.set_val(NRPPa_message)
        enc=M.to_aper()
        return enc
    except:
        log.logger_NRPPa.error('Error in encoding NRPPa message')
        return None

# TODO, not supported at the moment 
def handleE_CIDMeasurementInitiationResponse(body,nrppatransactionID):
    for i,item in enumerate(body):
        log.logger_NRPPa.debug(f"item number: {i}")
        id_IE = item['id']
        criticality=item['criticality']
        value = item['value']

        log.logger_NRPPa.debug(f'NRPPaIE  procedureCode {id_IE}')
        log.logger_NRPPa.debug(f' NRPPaIE  criticality: {criticality}')
        log.logger_NRPPa.debug(f'NRPPaIE  value: {value}')


    current_datetime = datetime.now(timezone.utc)
    formatted_timestamp = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")  
    ## TODO only to test the procedure for the moment, it returns a fixed estimation position
    result = { 'locationEstimate': {'shape': 'POINT','point': {'lat': 10, 'lon': 10 }}, 'timestampOfLocationEstimate': formatted_timestamp }
    return result


def handlePositioningInformationResponse(body,nrppatransactionID):
    
    lmf_istance=lmf.Lmf().get(nrppatransactionID)
    for i,item in enumerate(body):
        log.logger_NRPPa.debug(f"item number: {i}")
        id_IE = item['id']
        criticality=item['criticality']
        value = item['value']

        log.logger_NRPPa.debug(f'NRPPaIE  procedureCode {id_IE}')
        log.logger_NRPPa.debug(f' NRPPaIE  criticality: {criticality}')
        log.logger_NRPPa.debug(f'NRPPaIE  value: {value}')
        
        match (id_IE,value[0]):
            case (IEs_id.id_SRSConfiguration.value, "SRSConfiguration"):
                log.logger_NRPPa.debug(f'Save in DB the value[0]: {value[0]}')
                lmf_istance.SRSConfiguration = (IEs_id.id_SRSConfiguration.value,'SRSConfiguration', value[1])
            case (IEs_id.id_SFNInitialisationTime.value, "RelativeTime1900"):
                log.logger_NRPPa.debug(f'Save in DB the value[0]: {value[0]}')
                lmf_istance.RelativeTime1900 = (IEs_id.id_SFNInitialisationTime.value,'RelativeTime1900', value[1])
            case (IEs_id.id_UETxTEGAssociationList.value, "UETxTEGAssociationList"):
                log.logger_NRPPa.debug(f'Save in DB the value[0]: {value[0]}')
                lmf_istance.UETxTEGAssociationList = (IEs_id.id_UETxTEGAssociationList.value,'UETxTEGAssociationList', value[1])
    return 

def handlePositioningActivationResponse(body,nrppatransactionID):
    lmf_istance=lmf.Lmf().get(nrppatransactionID)
    for i,item in enumerate(body):
        log.logger_NRPPa.debug(f"item number: {i}")
        id_IE = item['id']
        criticality=item['criticality']
        value = item['value']

        log.logger_NRPPa.debug(f'NRPPaIE  procedureCode {id_IE}')
        log.logger_NRPPa.debug(f' NRPPaIE  criticality: {criticality}')
        log.logger_NRPPa.debug(f'NRPPaIE  value: {value}')

        match (id_IE,value[0]):
            case (IEs_id.id_SystemFrameNumber.value, "SystemFrameNumber"):
                log.logger_NRPPa.debug(f'Save in DB the value[0]: {value[0]}')
                lmf_istance.SystemFrameNumber = (IEs_id.id_SystemFrameNumber.value,'SystemFrameNumber', value[1])
            case (IEs_id.id_SlotNumber.value, "SlotNumber"):
                log.logger_NRPPa.debug(f'Save in DB the value[0]: {value[0]}')
                lmf_istance.SlotNumber = (IEs_id.id_SlotNumber.value,'SlotNumber', value[1])

    method = lmf_istance.mode_method["method"]
    mode = lmf_istance.mode_method["mode"]

    id_LMF_Measurement_ID = 1
    trpID = [config.trpID]
    reportCharacteristics = 'onDemand'
    timingReportingGranularityFactor= 1
    optional_fields=[]
    if hasattr(lmf_istance, 'RelativeTime1900'): 
        optional_fields.append(lmf_istance.RelativeTime1900)
    if hasattr(lmf_istance, 'SRSConfiguration'): 
        optional_fields.append(lmf_istance.SRSConfiguration)
    if hasattr(lmf_istance, 'SystemFrameNumber'): 
        optional_fields.append(lmf_istance.SystemFrameNumber)
    if hasattr(lmf_istance, 'SlotNumber'): 
        optional_fields.append(lmf_istance.SlotNumber)


    match method:
        case 'nr-Multi-RTT':
            tRPMeasurementQuantities =  'gNB-RxTxTimeDiff' #	uL-SRS-RSRP, 	uL-AoA, 	uL-RTOA,	...,	multiple-UL-AoA, 	uL-SRS-RSRPP
            nrppa_message = gen_nrppa.MeasurementRequest(nrppatransactionID,id_LMF_Measurement_ID,trpID,reportCharacteristics,tRPMeasurementQuantities ,timingReportingGranularityFactor, optional_fields)
        case 'nr-UL-TDOA':
            tRPMeasurementQuantities =  'uL-RTOA' #	uL-SRS-RSRP, 	uL-AoA, 	uL-RTOA,	...,	multiple-UL-AoA, 	uL-SRS-RSRPP
            nrppa_message = gen_nrppa.MeasurementRequest(nrppatransactionID,id_LMF_Measurement_ID,trpID,reportCharacteristics,tRPMeasurementQuantities ,timingReportingGranularityFactor, optional_fields)
        case 'nr-UL-AoA':
            tRPMeasurementQuantities =  'uL-AoA'#	'gNB-RxTxTimeDiff' #	uL-SRS-RSRP, 	uL-AoA, 	uL-RTOA,	...,	multiple-UL-AoA, 	uL-SRS-RSRPP
            nrppa_message = gen_nrppa.MeasurementRequest(nrppatransactionID,id_LMF_Measurement_ID,trpID,reportCharacteristics,tRPMeasurementQuantities ,timingReportingGranularityFactor, optional_fields)
    return nrppa_message


def handleMeasurementResponse(body,nrppatransactionID):
    lmf_istance=lmf.Lmf().get(nrppatransactionID)
    method= lmf_istance.mode_method["method"]
    value = body[0]['value'][1]

    if config.FLAG_LATENCY_STUDTY:

        
        measurement_nrppa_gNB = [2.3112e-6, 2.5879e-6, 2.9948e-6, 1.6683e-6] # Misure TOA in secondi
        
        #gNBPos= [{'x': 153.5898,'y': 700},             
        # {'x': 153.5898,'y':500},
        # {'x': 153.5898,'y':300},
        # {'x': 326.7949,'y':800}]
        
        lmf_istance.Add_NRPPa_measurement(measurement_nrppa_gNB)
        # result = {"locationEstimate":{ "shape":"POINT",
        #                                 "point":{"lon":23.7255,
        #                                         "lat": 37.972}},
        #           'timestampOfLocationEstimate' : datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")}
        # result.update({'transaction_number': nrppatransactionID })
        # return {'result':result}
        if len(lmf_istance.NRPPa_measurements) >= config.NumberMeasNRPPaRequest:
            log.logger_NRPPa.info(f'Reached the number of measurements requested: {config.NumberMeasNRPPaRequest}')
            try:
                log.set_timestamp({'T5':time.time()})
                result = HandleLocation.handle_NRPPa_measurements(lmf_istance.NRPPa_measurements,method)
                result.update({'transaction_number': nrppatransactionID })
                if result == {}:
                    return {'result':"ERROR"}
                return {'result':result}
            except Exception as e:
                log.logger_NRPPa.error(f'Error in handling Measurement Response with error: {e}')
                return {'result':"ERROR"}      
        else:
            return {"none":"none"}
    else:
        measurement_nrppa_gNB= HandleLocation.Extract_and_Save_NRPPa_measurements(value,method)
        lmf_istance=lmf.Lmf().get(nrppatransactionID)
        lmf_istance.Add_NRPPa_measurement(measurement_nrppa_gNB)

        if len(lmf_istance.NRPPa_measurements) >= config.NumberMeasNRPPaRequest:
            log.logger_NRPPa.info(f'Reached the number of measurements requested: {config.NumberMeasNRPPaRequest}')
            try:
                result = HandleLocation.handle_NRPPa_measurements(lmf_istance.NRPPaMeasurement,method)
                result.update({'transaction_number': nrppatransactionID })
                if result == {}:
                    return {'result':"ERROR"}
                return {'result':result}
            except Exception as e:
                log.logger_NRPPa.error(f'Error in handling Measurement Response with error: {e}')
                return {'result':"ERROR"}      
        else:
            return {"none":"none"}

def handleInitialMessage(Body):
    global UEassociatedMessage_FLAG
    keys = ["procedureCode","criticality" , "nrppatransactionID", "value"]
    if not all(field in Body for field in keys):
        ResponseLPP_Message_body= "error" 
        log.logger_NRPPa.error(f'Missing fields in SuccessfulOutcome NRPPa MESSAGE')
        return ResponseLPP_Message_body

    procedureCode = Body['procedureCode']
    criticality=Body['criticality']
    nrppatransactionID= Body['nrppatransactionID']
    value = Body['value']

    log.logger_NRPPa.debug(f'NRPPa  procedureCode {procedureCode} -> {ProcedureCodeEP(procedureCode).name} ')
    log.logger_NRPPa.debug(f'NRPPa  criticality: {criticality}')
    log.logger_NRPPa.debug(f'NRPPa  nrppatransactionID: {nrppatransactionID}')
    log.logger_NRPPa.debug(f'NRPPa  value: {value}')


    typeNRPPaBody=value[0]
    NRPPaBodyMessage=value[1]

    bodyIEs= NRPPaBodyMessage['protocolIEs']

    match (typeNRPPaBody, procedureCode):
        case ('E-CIDMeasurementInitiationRequest',ProcedureCodeEP.id_e_CIDMeasurementInitiation.value): # initianing message
            log.logger_NRPPa.error(f'This type of NRPPa EP {typeNRPPaBody} can not be received by the LMF')  
            return "error"
        case ('E-CIDMeasurementFailureIndication',ProcedureCodeEP.id_e_CIDMeasurementFailureIndication.value): # initianing
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Received an E-CIDMeasurementFailureIndication messages')
              
            return "error"
            # Call function to handle E-CID Measurement Failure Indication
        case ('E-CIDMeasurementReport',ProcedureCodeEP.id_e_CIDMeasurementReport.value): # initianing
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            # TODO  # Call function to handle E-CID Measurement Report      
            return "error"
        case ('E-CIDMeasurementTermination',ProcedureCodeEP.id_e_CIDMeasurementTermination.value): # initianing
            log.logger_NRPPa.error(f'This type of NRPPa EP {typeNRPPaBody} can not be received by the LMF')  
            return "error"
        case ('OTDOAInformationRequest',ProcedureCodeEP.id_oTDOAInformationExchange.value):   
            log.logger_NRPPa.error(f'This type of NRPPa EP {typeNRPPaBody} can not be received by the LMF')  
            return "error"
        case ('AssistanceInformationControl',ProcedureCodeEP.id_assistanceInformationControl.value):
            log.logger_NRPPa.error(f'This type of NRPPa EP {typeNRPPaBody} can not be received by the LMF')  
            return "error"
        case ('AssistanceInformationFeedback',ProcedureCodeEP.id_assistanceInformationFeedback.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            return "error"        
        case('ErrorIndication',ProcedureCodeEP.id_errorIndication.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            return "error"
        case('PrivateMessage',ProcedureCodeEP.id_privateMessage.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            
            return "error"
        case ('PositioningInformationRequest',ProcedureCodeEP.id_positioningInformationExchange.value): 
            log.logger_NRPPa.error(f'This type of NRPPa EP {typeNRPPaBody} can not be received by the LMF')  
            return "error"
        case ('PositioningInformationUpdate',ProcedureCodeEP.id_positioningInformationUpdate.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            return "error"
        case ('MeasurementRequest', ProcedureCodeEP.id_Measurement.value):
            log.logger_NRPPa.error(f'This type of NRPPa EP {typeNRPPaBody} can not be received by the LMF')  
            return "error"
        case ('MeasurementReport',ProcedureCodeEP.id_MeasurementReport.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            return "error"
        case ('MeasurementUpdate',ProcedureCodeEP.id_MeasurementUpdate.value):
            log.logger_NRPPa.error(f'This type of NRPPa EP {typeNRPPaBody} can not be received by the LMF')  
            return "error" 
        case ('MeasurementAbort',ProcedureCodeEP.id_MeasurementAbort.value):
            log.logger_NRPPa.error(f'This type of NRPPa EP {typeNRPPaBody} can not be received by the LMF')  
            return "error"
        case ('MeasurementFailureIndication',ProcedureCodeEP.id_MeasurementFailureIndication.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            return "error"
        case ('TRPInformationRequest',ProcedureCodeEP.id_tRPInformationExchange.value): 
            log.logger_NRPPa.error(f'This type of NRPPa EP {typeNRPPaBody} can not be received by the LMF')  
            return "error"
        case ('PositioningActivationRequest',ProcedureCodeEP.id_positioningActivation.value): 
            log.logger_NRPPa.error(f'This type of NRPPa EP {typeNRPPaBody} can not be received by the LMF')              
            return "error"
        case ('PositioningDeactivation',ProcedureCodeEP.id_positioningDeactivation.value):
            log.logger_NRPPa.error(f'This type of NRPPa EP {typeNRPPaBody} can not be received by the LMF')  
            return "error"
        case ('PRSConfigurationRequest',ProcedureCodeEP.id_pRSConfigurationExchange.value): 
            log.logger_NRPPa.error(f'This type of NRPPa EP {typeNRPPaBody} can not be received by the LMF')  
            return "error"
        case ('MeasurementPreconfigurationRequired',ProcedureCodeEP.id_measurementPreconfiguration.value):
            log.logger_NRPPa.error(f'This type of NRPPa EP {typeNRPPaBody} can not be received by the LMF')  
            return "error"
        case ('MeasurementActivation',ProcedureCodeEP.id_measurementActivation.value):
            log.logger_NRPPa.error(f'This type of NRPPa EP {typeNRPPaBody} can not be received by the LMF')  
            return "error"
        case (_,_):
            log.logger_NRPPa.error(f'Undefineded type of NRPPa EP Received {typeNRPPaBody} and/or procedureCode incorect with EP {procedureCode}')
            return "error"
    return 'ok'

def handleSuccessfulOutcome(Body):
    global UEassociatedMessage_FLAG

    keys= ["procedureCode","criticality" , "nrppatransactionID", "value"]
    if not all(field in Body for field in keys):
        log.logger_NRPPa.error(f'Missing fields in SuccessfulOutcome NRPPa MESSAGE')
        return {'error':"ERROR"}

    procedureCode = Body['procedureCode']
    criticality=Body['criticality']
    nrppatransactionID= Body['nrppatransactionID']
    value = Body['value']

    log.logger_NRPPa.debug(f'NRPPa  procedureCode {procedureCode} -> {ProcedureCodeEP(procedureCode).name} ')
    log.logger_NRPPa.debug(f'NRPPa  criticality: {criticality}')
    log.logger_NRPPa.debug(f'NRPPa  nrppatransactionID: {nrppatransactionID}')
    log.logger_NRPPa.debug(f'NRPPa  value: {value}')

    typeNRPPaBody=value[0]
    NRPPaBodyMessage=value[1]

    bodyIEs= NRPPaBodyMessage['protocolIEs']

    match (typeNRPPaBody, procedureCode):
        case ('E-CIDMeasurementInitiationResponse',ProcedureCodeEP.id_e_CIDMeasurementInitiation.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            try:
                result = handleE_CIDMeasurementInitiationResponse(bodyIEs,nrppatransactionID)
                result.update({'transaction_number': nrppatransactionID })
                return {'result':result}
            except:
                log.logger_NRPPa.error('Error in handling E-CID Measurement Initiation Response')
                return {'error':"ERROR"}

        case ('OTDOAInformationResponse',ProcedureCodeEP.id_oTDOAInformationExchange.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            # TODO  # Call function to handle OTDOA Information Response        
            return {'error':"ERROR"}
        
        case ('PositioningInformationResponse',ProcedureCodeEP.id_positioningInformationExchange.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            try:
                handlePositioningInformationResponse(bodyIEs,nrppatransactionID)
                SRSType = ('aperiodicSRS', { 'aperiodic': 'true'})
                nrppa_message = gen_nrppa.PositioningActivationRequest(nrppatransactionID,SRSType)
                # based on the information received and saved in the LMF_DATABASE
                return {'nrrpa_message':nrppa_message}
            except:
                log.logger_NRPPa.error('Error in handling Positioning Information Response')
                return {'error':"ERROR"}

        case ('MeasurementResponse',ProcedureCodeEP.id_Measurement.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            result = handleMeasurementResponse(bodyIEs,nrppatransactionID)
            return result
    

        case ('TRPInformationResponse',ProcedureCodeEP.id_tRPInformationExchange.value):
            # Call function to handle TRP Information Response
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            # TODO  # Call function to handle TRPInformationResponse     
            return {'error':"ERROR"}

        case ('PositioningActivationResponse',ProcedureCodeEP.id_positioningActivation.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            try:
                nrppa_message= handlePositioningActivationResponse(bodyIEs,nrppatransactionID)
                UEassociatedMessage_FLAG = False
                return {'nrrpa_message':nrppa_message}
            except:
                log.logger_NRPPa.error('Error in handling Positioning Activation Response')
                return {'error':"ERROR"}

            # Call function to handle Positioning Activation Response
        case ('PRSConfigurationResponse',ProcedureCodeEP.id_pRSConfigurationExchange.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            # TODO  # Call function to handle PRSConfigurationResponse       
            return {'error':"ERROR"}

        case ('MeasurementPreconfigurationConfirm',ProcedureCodeEP.id_measurementPreconfiguration.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            # TODO  # Call function to handle MeasurementPreconfigurationConfirm       
            return {'error':"ERROR"}
        case (_,_):
            log.logger_NRPPa.error(f'Undefineded type of EP Received {typeNRPPaBody} and/or procedureCode incorect with EP {procedureCode}')
            return {'error':"ERROR"}
    return {'error':"ERROR"}

def handleUnsuccessfulOutcome(Body):
    global UEassociatedMessage_FLAG
    keys= ["procedureCode","criticality" , "nrppatransactionID", "value"]
    if not all(field in Body for field in keys):
        log.logger_NRPPa.error(f'Missing fields in SuccessfulOutcome NRPPa MESSAGE')
        return 

    procedureCode = Body['procedureCode']
    criticality=Body['criticality']
    nrppatransactionID= Body['nrppatransactionID']
    value = Body['value']

    log.logger_NRPPa.debug(f'NRPPa  procedureCode {procedureCode} -> {ProcedureCodeEP(procedureCode).name} ')
    log.logger_NRPPa.debug(f'NRPPa  criticality: {criticality}')
    log.logger_NRPPa.debug(f'NRPPa  nrppatransactionID: {nrppatransactionID}')
    log.logger_NRPPa.debug(f'NRPPa  value: {value}')

    typeNRPPaBody=value[0]
    NRPPaBodyMessage=value[1]

    bodyIEs= NRPPaBodyMessage['protocolIEs']

    match (typeNRPPaBody, procedureCode):
        case ('E-CIDMeasurementInitiationFailure',ProcedureCodeEP.id_e_CIDMeasurementInitiation.value): # unsuccessful
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
        case ('OTDOAInformationFailure',ProcedureCodeEP.id_oTDOAInformationExchange.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            # Call function to handle OTDOA Information Failure        
        case ('PositioningInformationFailure',ProcedureCodeEP.id_positioningInformationExchange.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            # Call function to handle Positioning Information Failure
        case ('MeasurementFailure',ProcedureCodeEP.id_Measurement.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            # Call function to handle Measurement Failure
        case ('TRPInformationFailure',ProcedureCodeEP.id_tRPInformationExchange.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            # Call function to handle TRP Information Failure
        case ('PositioningActivationFailure',ProcedureCodeEP.id_positioningActivation.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            # Call function to handle Positioning Activation Failure
        case ('PRSConfigurationFailure',ProcedureCodeEP.id_pRSConfigurationExchange.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            # Call function to handle PRS Configuration Failure
        case ('MeasurementPreconfigurationRefuse',ProcedureCodeEP.id_measurementPreconfiguration.value):
            log.logger_NRPPa.info(f'Handling {typeNRPPaBody} type of EP')
            log.logger_NRPPa.warning(f'Not currently implemented the {typeNRPPaBody} procedure')
            # Call function to handle Measurement Preconfiguration Refuse

    try:
        for i,item in enumerate(bodyIEs):
            log.logger_NRPPa.debug(f"item number: {i}")
            id_IE = item['id']
            criticality=item['criticality']
            value = item['value']
            log.logger_NRPPa.debug(f' {typeNRPPaBody}  procedureCode {id_IE}')
            log.logger_NRPPa.debug(f' {typeNRPPaBody}  criticality: {criticality}')
            log.logger_NRPPa.debug(f'{typeNRPPaBody}  value: {value}')
    except:
        log.logger_NRPPa.error(f'Error in handling {typeNRPPaBody} UnsuccessfulOutcome messages')
    log.logger_NRPPa.error(f'Estimation is aborted by an UnsuccessfulOutcome messages')

    return "error"

def handlerNRPPa(nrppa_message_asn):
    global UEassociatedMessage_FLAG

    ## Flag
    END_FLAG_LOCATION=False
    ABORT_FLAG= False
    log.logger_NRPPa.info('Start handling a NRPPa message')
    nrppa_message= decodeNRPPa(nrppa_message_asn)

    if nrppa_message == None:
        return "ERROR"

    message_type=nrppa_message[0]
    body_message=nrppa_message[1]
    log.logger_NRPPa.debug(f"message type body ----> {message_type}")
    log.logger_NRPPa.debug(f"entire body ----> {body_message}")

    nrppatransactionID = body_message['nrppatransactionID']
    lmf_istance=lmf.Lmf().get(nrppatransactionID)

    match message_type :

        case 'initiatingMessage':
            log.logger_NRPPa.info(f'Handled of {message_type} NRPPa procedure' )
            try:
                result = handleInitialMessage(body_message)
            except:
                log.logger_NRPPa.error('Error in handling Initial NRPPa message')      
                result = "error"

            match result: 
                case "ok":
                    ResponseNRPPa_Message={}
                case "error":
                    nrppa_message=gen_nrppa.ErrorIndication(nrppatransactionID,('misc', 'unspecified' ))
                    ABORT_FLAG=True         


        case 'successfulOutcome':
            log.logger_NRPPa.info(f'Handled of {message_type} NRPPa procedure' )
            try:
                response = handleSuccessfulOutcome(body_message)
            except:
                log.logger_NRPPa.error('Error in handling Successful NRPPa message')
                response = {'error':"ERROR"}

            first_key = next(iter(response.keys()))

            match first_key:
                case 'result':

                    if response['result'] == "ERROR":
                        log.logger_NRPPa.error('Error computing the estimation')
                        ABORT_FLAG=True
                    END_FLAG_LOCATION=True
                    result=response['result']
                case 'nrrpa_message':
                    ResponseNRPPa_Message=response['nrrpa_message']
                case 'error':
                    ResponseNRPPa_Message={'nrrpa_message', gen_nrppa.ErrorIndication(nrppatransactionID,('misc', 'unspecified' )) }
                    ABORT_FLAG=True
                case "none":
                    return "OK"                           
        
        case 'unsuccessfulOutcome': 
            log.logger_NRPPa.info(f'Handled of {message_type} NRPPa procedure' )
            try:
                handleUnsuccessfulOutcome(body_message)
                ResponseNRPPa_Message={}
            except:
                log.logger_NRPPa.error('Error in handling Unsuccessful NRPPa message')
                ResponseNRPPa_Message={'nrrpa_message', gen_nrppa.ErrorIndication(nrppatransactionID,('misc', 'unspecified' )) }
            ABORT_FLAG=True

        case _:
            log.logger_NRPPa.error(f'Missing fields in SuccessfulOutcome NRPPa MESSAGE')
            ResponseNRPPa_Message = {}
            ABORT_FLAG=True
    
    if END_FLAG_LOCATION == True:
        # the estimation is conclude, send the notify to the thread that respond to the initial HTTP request
        log.logger_NRPPa.info('END ESTIMATION PROCESS BY ESTIMATION COMPLETE')
        log.logger_NRPPa.info(f'Estimation position:{result}')
        lmf.estimation_procedure_completed(result)
        END_FLAG_LOCATION=False
        return "END"
    
    if ResponseNRPPa_Message != {}:
        log.logger_NRPPa.debug(f'ResponseLPP_Message_body: {ResponseNRPPa_Message}')
        nrppa_message_asn= encodeNRPPa(ResponseNRPPa_Message)  
        log.logger_NRPPa.debug(nrppa_message_asn)  

        if UEassociatedMessage_FLAG or True:
            lmf.send_message(nrppa_message_asn,proto="ngap", imsi=lmf_istance.imsi)
        else:
            lmf.send_nonUEassociated(nrppa_message_asn)

    if ABORT_FLAG:
        log.logger_NRPPa.info('END ESTIMATION PROCESS BY ABORT PROCEDURE')
        # send the notify to the thread that respond to the initial HTTP request with error
        lmf.estimation_procedure_error({'transaction_number': nrppatransactionID })
        return "ERROR"

    return "OK"