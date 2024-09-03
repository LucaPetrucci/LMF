from pycrate_asn1dir import LPP
import copy
import custom_log as log
import lmf_instance as lmf
import LPP_message_gen as lpp_gen
import NRPPa_message_gen as nrppa_gen
import NRPPa_handler 
from HandleLocation import *

def encodeLPP(lpp_message):
    try:
        #encode the lpp messagge to asn1
        log.logger_LPP.info('Encoding the LPP message')
        M = LPP.LPP_PDU_Definitions.LPP_Message
        M.set_val(lpp_message)
        LPP_message_ANS1 = M.to_uper()  
        return LPP_message_ANS1
    except Exception as e:
        log.logger_LPP.error(f'Error during encoding the LPP message: {e}')
        return None

def decodeLPP(LPP_message_ANS1):
    try:
        #decode the lpp messagge from asn1
        log.logger_LPP.info('Deconding the LPP message')
        M = LPP.LPP_PDU_Definitions.LPP_Message
        M.from_uper(LPP_message_ANS1)
        decoded_message_LPP = copy.deepcopy(M())
        return decoded_message_LPP
    except:
        log.logger_LPP.error('Error during decoding the LPP message')
        return None


def extractPosModeSupported(mode_received,otdoa=False):
    if otdoa:
        bin_mode = bin(mode_received[0])[2:]
        supported_modes = []
        mode=['UE-assisted','UE-Assisted-NB-r14','UE-Assisted-NB-TDD-r15']
        for i in range(len(bin_mode)):
            if bin_mode[i]=='1':
                supported_modes.append(mode[i])

    else:
        bin_mode = format(mode_received[0], '08b')
        supported_modes = []
        mode=['Standalone','UE-Based','UE-Assisted']
        for i in range(len(bin_mode)):
            if bin_mode[i]=='1':
                supported_modes.append(mode[i])
    return supported_modes


# HANDLER OF PROVIDE CAPABILITIES
def handle_provide_capabilities(body):
    if body['criticalExtensions'][0] == 'c1':
        mode_method_supported=[]
        message_body = body['criticalExtensions'][1]
        if message_body[0]== 'provideCapabilities-r9':
            ProvideCabailities=message_body[1]
            for items in ProvideCabailities:
                match items:
                    case 'commonIEsProvideCapabilities':
                        BodyX= ProvideCabailities[items]
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Info provide capabilities on {items2}')

                    case 'a-gnss-ProvideCapabilities':
                        log.logger_LPP.info(f'Methods supported {items}')
                        BodyX= ProvideCabailities[items]
                        mode_received=  BodyX['gnss-SupportList'][0]['agnss-Modes']['posModes']
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Info provide capabilities on {items2}')                        
                        try:
                            supported_modes= extractPosModeSupported(mode_received)
                            info_method={'method':'a-gnss',  'mode':supported_modes}
                            mode_method_supported.append(info_method)
                        except:
                            log.logger_LPP.error('Error during extractPosModeSupported function')

                    case 'otdoa-ProvideCapabilities':
                        log.logger_LPP.info(f'Methods supported {items}')
                        BodyX= ProvideCabailities[items]
                        mode_received=  BodyX['otdoa-Mode']

                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Info provide capabilities on {items2}')
                        try:
                            supported_modes= extractPosModeSupported(mode_received,otdoa=True)
                            info_method={'method':'otdoa',  'mode':supported_modes}
                            mode_method_supported.append(info_method)
                        except:
                            log.logger_LPP.error('Error during extractPosModeSupported function')

                    case 'ecid-ProvideCapabilities':
                        log.logger_LPP.info(f'Methods supported {items}')
                        info_method={'method':'ecid',  'mode':['UE-Assisted','Network-based']}
                        mode_method_supported.append(info_method)
                        BodyX= ProvideCabailities[items]
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Info provide capabilities on {items2}')

                    case 'epdu-ProvideCapabilities':
                        log.logger_LPP.info(f'Methods supported {items}')
                        BodyX= ProvideCabailities[items]
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Info provide capabilities on {items2}')

                    case 'sensor-ProvideCapabilities-r13':
                        log.logger_LPP.info(f'Methods supported {items}')
                        BodyX= ProvideCabailities[items]
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Info provide capabilities on {items2}')

                    case 'tbs-ProvideCapabilities-r13':
                        log.logger_LPP.info(f'Methods supported {items}')
                        BodyX= ProvideCabailities[items]
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Info provide capabilities on {items2}')

                    case 'wlan-ProvideCapabilities-r13':
                        log.logger_LPP.info(f'Methods supported {items}')
                        BodyX= ProvideCabailities[items]
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Info provide capabilities on {items2}')

                    case 'bt-ProvideCapabilities-r13':
                        log.logger_LPP.info(f'Methods supported {items}')
                        BodyX= ProvideCabailities[items]
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Info provide capabilities on {items2}')

                    case 'nr-ECID-ProvideCapabilities-r16':
                        log.logger_LPP.info(f'Methods supported {items}')
                        info_method={'method':'nr-ECID',  'mode':['UE-Assisted','Network-based']}
                        mode_method_supported.append(info_method)
                        BodyX= ProvideCabailities[items]
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Info provide capabilities on {items2}')
                    case 'nr-Multi-RTT-ProvideCapabilities-r16':
                        log.logger_LPP.info(f'Methods supported {items}')
                        info_method={'method':'nr-Multi-RTT',  'mode':['UE-Assisted','Network-based']}
                        mode_method_supported.append(info_method)
                        BodyX= ProvideCabailities[items]
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Info provide capabilities on {items2}')
                        Body_PRS_PRO_CAP=BodyX['nr-DL-PRS-ProcessingCapability-r16']
                        capabilities_prs_processing=[]
                        for procBandList_item in Body_PRS_PRO_CAP['prs-ProcessingCapabilityBandList-r16']:
                                capabilities_prs_processing_item={}
                                capabilities_prs_processing_item.update({'freqBandIndicatorNR-r16':procBandList_item['freqBandIndicatorNR-r16']})
                                capabilities_prs_processing_item.update({'supportedBandwidthPRS-r16': {procBandList_item['supportedBandwidthPRS-r16'][0]:procBandList_item['supportedBandwidthPRS-r16'][1] }})
                                capabilities_prs_processing_item.update({'maxNumOfDL-PRS-ResProcessedPerSlot-r16':procBandList_item['maxNumOfDL-PRS-ResProcessedPerSlot-r16']})
                                capabilities_prs_processing.append(capabilities_prs_processing_item)

                    case 'nr-DL-AoD-ProvideCapabilities-r16':
                        log.logger_LPP.info(f'Methods supported {items}')
                        BodyX= ProvideCabailities[items]
                        mode_received=  BodyX['nr-DL-TDOA-Mode-r16']['posModes']
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Info provide capabilities on {items2}')

                        try:
                            supported_modes= extractPosModeSupported(mode_received)
                            info_method={'method':'nr-DL-AoD',  'mode':supported_modes}
                            mode_method_supported.append(info_method)
                        except:
                            log.logger_LPP.error('Error during extractPosModeSupported function')


                    case 'nr-DL-TDOA-ProvideCapabilities-r16':
                        log.logger_LPP.info(f'Methods supported {items}')
                        BodyX= ProvideCabailities[items]
                        #'nr-DL-TDOA-Mode-r16': {'posModes': (2,8)}, 
                        '''standalone -> 128,ue-based -> 64,ue-assisted -> 32'''
                        mode_received=  BodyX['nr-DL-TDOA-Mode-r16']['posModes']
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Info provide capabilities on {items2}')
                        
                        try:
                            supported_modes= extractPosModeSupported(mode_received)
                            info_method={'method':'nr-DL-TDOA',  'mode':supported_modes}
                            mode_method_supported.append(info_method)
                        except:
                            log.logger_LPP.error('Error during extractPosModeSupported function')
                            
                    case 'nr-UL-ProvideCapabilities-r16':
                        log.logger_LPP.info(f'Methods supported {items}')
                        BodyX= ProvideCabailities[items]
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Info provide capabilities on {items2}')
                    case _:
                        log.logger_LPP.error(f' No Provide capabilities for this {items} method')
                        result=  {'mode': 'error', 'method': 'error' }                      
        else:
            log.logger_LPP.error('handling provide capabilities messages')
            result= {'mode': 'error', 'method': 'error' } 
    else:
        log.logger_LPP.error('handling provide capabilities messages')
        result=  {'mode': 'error', 'method': 'error' }  


    log.logger_LPP.info('Method Supported by the UE are:')
    for i in mode_method_supported:
        log.logger_LPP.info(i)
    return mode_method_supported


# HANDLER OF REQUEST ASSISTANCE DATA
def handle_request_assistance_data(body):

    if body['criticalExtensions'][0] == 'c1':
        message_body = body['criticalExtensions'][1]
        if message_body[0]== 'requestAssistanceData-r9':
            RequestAssistanceData=message_body[1]
            for items in RequestAssistanceData:
                match items:
                    case 'commonIEsRequestAssistanceData':
                        log.logger_LPP.info(f'Requested assistance data for {items}')
                        BodyX= RequestAssistanceData[items]
                        for items2 in BodyX:
                            print("Assistance data requested ", items2)
                    case 'a-gnss-RequestAssistanceData':
                        log.logger_LPP.info(f'Requested assistance data for {items} method')
                        log.logger_LPP.warning("Not supported method at the moment")                    
                    case 'otdoa-RequestAssistanceData':
                        log.logger_LPP.info(f'Requested assistance data for {items} method')
                        log.logger_LPP.warning("Not supported method at the moment")     
                    case 'epdu-RequestAssistanceData':
                        log.logger_LPP.info(f'Requested assistance data for {items} method')
                        log.logger_LPP.warning("Not supported method at the moment")                         
                    case 'sensor-RequestAssistanceData-r14':
                        log.logger_LPP.info(f'Requested assistance data for {items} method')
                        log.logger_LPP.warning("Not supported method at the moment")     
                    case 'tbs-RequestAssistanceData-r14':
                        log.logger_LPP.info(f'Requested assistance data for {items} method')
                        log.logger_LPP.warning("Not supported method at the moment")     
                    case 'wlan-RequestAssistanceData-r14':
                        log.logger_LPP.info(f'Requested assistance data for {items} method')
                        log.logger_LPP.warning("Not supported method at the moment")                         
                    case 'nr-Multi-RTT-RequestAssistanceData-r16':
                        log.logger_LPP.info(f'Requested assistance data for {items} method')
                        BodyX= RequestAssistanceData[items]

                        #info_needed=extract_info_neded(BodyX['nr-AdType-r16']) # TODO

                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Assistance data requested: {items2}')
                            # CALL FUNCTION TO NRPPa PROCEDURE TO OBTAIN THE REQUEST                        
                        result = lpp_gen.generate_lpp_provide_assistance_data(items)
                        log.logger_LPP.debug(f'Assistance data provided: {result}')

                    case 'nr-DL-AoD-RequestAssistanceData-r16':
                        log.logger_LPP.info(f'Requested assistance data for {items} method')
                        BodyX= RequestAssistanceData[items]
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Assistance data requested: {items2}')
                        log.logger_LPP.warning("Not supported method at the moment")                         

                    case 'nr-DL-TDOA-RequestAssistanceData-r16':
                        log.logger_LPP.info(f'Requested assistance data for {items} method')
                        BodyX= RequestAssistanceData[items]
                        for items2 in BodyX:
                            log.logger_LPP.debug(f'Assistance data requested: {items2}')
                        
                        result = lpp_gen.generate_lpp_provide_assistance_data(items)
                        log.logger_LPP.debug(f'Assistance data provided: {result}')                        

                    case _:
                        log.logger_LPP.error('No assistance data for this {items} method')
                        result = 'error'
        else:
            log.logger_LPP.error('handling assistance data messages')
            result = 'error' 
    else:
            log.logger_LPP.error('handling assistance data messages')
            result = 'error' 

    return result


# HANDLER OF PROVIDE LOCATION INFORMATION
def handle_provide_location_information(body):

    if body['criticalExtensions'][0] == 'c1':
        message_body = body['criticalExtensions'][1]
        if message_body[0]== 'provideLocationInformation-r9':
            ProvideLocationInformation=message_body[1]
            for items in ProvideLocationInformation:
                match items:
                    case 'commonIEsProvideLocationInformation':
                        BodyX= ProvideLocationInformation[items]
                        log.logger_LPP.info(f'Result of estimation is {BodyX}')
                        result = BodyX 
                        
                    case 'a-gnss-ProvideLocationInformation':
                        log.logger_LPP.info(f' Received information on {items} ')
                        log.logger_LPP.warning(f'Not supported: information for this {items} method ')
                        result = 'error'                                        
                
                    case 'otdoa-ProvideLocationInformation':
                        log.logger_LPP.info(f' Received information on {items} ')
                        log.logger_LPP.warning(f'Not supported: information for this {items} method ')
                        result = 'error'

                    case 'ecid-ProvideLocationInformation':
                        log.logger_LPP.info(f' Received information on {items} ')
                        log.logger_LPP.warning(f'Not supported: information for this {items} method ')
                        result = 'error'

                    case 'epdu-ProvideLocationInformation': 
                        log.logger_LPP.info(f' Received information on {items} ')
                        log.logger_LPP.warning(f'Not supported: information for this {items} method ')
                        result = 'error'

                    case 'sensor-ProvideLocationInformation-r13':
                        log.logger_LPP.info(f' Received information on {items} ')
                        log.logger_LPP.warning(f'Not supported: information for this {items} method ')
                        result = 'error'

                    case 'tbs-ProvideLocationInformation-r13':
                        log.logger_LPP.info(f' Received information on {items} ')
                        log.logger_LPP.warning(f'Not supported: information for this {items} method ')
                        result = 'error'

                    case 'wlan-ProvideLocationInformation-r13':
                        log.logger_LPP.info(f' Received information on {items} ')
                        log.logger_LPP.warning(f'Not supported: information for this {items} method ')
                        result = 'error'

                    case 'bt-ProvideLocationInformation-r13':
                        log.logger_LPP.info(f' Received information on {items} ')
                        log.logger_LPP.warning(f'Not supported: information for this {items} method ')
                        result = 'error'

                    case 'nr-ECID-ProvideLocationInformation-r16':
                        log.logger_LPP.info(f' Received information on {items} ')
                        log.logger_LPP.warning(f'Not supported: information for this {items} method ')
                        result = 'error'

                    case 'nr-Multi-RTT-ProvideLocationInformation-r16':
                        log.logger_LPP.info(f' Received information on {items} ')
                        BodyX= ProvideLocationInformation[items]
                        for items2 in BodyX:
                            match items2:
                                case 'nr-Multi-RTT-SignalMeasurementInformation-r16':
                                    
                                    RTT_List_Meas= BodyX[items2]['nr-Multi-RTT-MeasList-r16']
                                    print("Number of RTT Measurement are: ", len(RTT_List_Meas))
                                    log.logger_LPP.debug(f'Number of RTT Measurement are: {len(RTT_List_Meas)}')
                                    # CALL FUNCTION TO COMPUTE THE ESTIMATION
                                    try:
                                        result= handle_RTT_measurements(RTT_List_Meas)
                                    except:
                                        log.logger_LPP.error('Error during handle_RTT_measurements function')
                                        result = 'error'
                                
                                case 'nr-Multi-RTT-Error-r16':
                                    log.logger_LPP.debug(f'{items2}: are {BodyX[items2]}')
                                case 'nr-Multi-RTT-SignalMeasurementInstances-r17':
                                    log.logger_LPP.debug(f'{items2}: are {BodyX[items2]}')

                    case 'nr-DL-AoD-ProvideLocationInformation-r16':
                        log.logger_LPP.info(f'Received information on {items} ')
                        log.logger_LPP.warning(f'Not supported: information for this {items} method ')
                        result = 'error'

                    case 'nr-DL-TDOA-ProvideLocationInformation-r16':
                        log.logger_LPP.info( f'Received information on {items} ')
                        BodyX= ProvideLocationInformation[items]
                        for items2 in BodyX:
                            match items2:
                                case 'nr-DL-TDOA-SignalMeasurementInformation-r16':
                                    PRS_ID_Reference= BodyX[items2]['dl-PRS-ReferenceInfo-r16']

                                    TOA_List_Meas= BodyX[items2]['nr-DL-TDOA-MeasList-r16']
                                    log.logger_LPP.debug(f'Number of DL-TDOA Measurement are: {len(TOA_List_Meas)-1}')
                                    try:
                                        result= handle_TDOA_measurements(PRS_ID_Reference,TOA_List_Meas)
                                    except:
                                        log.logger_LPP.error('Error during handle_TDOA_measurements function')
                                        result = 'error'
                    
                                case 'nr-dl-tdoa-LocationInformation-r16':
                                    log.logger_LPP.debug(f'{items2}: are {BodyX[items2]}')
                                case 'nr-DL-TDOA-Error-r16':
                                    log.logger_LPP.debug(f'{items2}: are {BodyX[items2]}')
                                case 'nr-DL-TDOA-SignalMeasurementInstances-r17':
                                    log.logger_LPP.debug(f'{items2}: are {BodyX[items2]}')
                                case 'nr-DL-TDOA-LocationInformationInstances-r17':
                                    log.logger_LPP.debug(f'{items2}: are {BodyX[items2]}')
                           
                    case _:
                        log.logger_LPP.error(f' No Provide Location information data for this {items} method')
                        result = 'error'
       
        else:
            log.logger_LPP.error('Handling assistance data messages')
            result = 'error' 
    else:
            log.logger_LPP.error('Handling assistance data messages')
            result = 'error' 

    return result


# HANDLER OF ERROR
def handle_error(body):
    errorBody= body[1]
    for items in errorBody:
        match items:
            case 'commonIEsError':
                log.logger_LPP.warning(f'Received this error: {errorBody[items]["errorCause"]}')
            case 'epdu-Error':
                log.logger_LPP.warning(f'Received this error on {items}')
            case _:
                log.logger_LPP.error('Handling on Error messages')
    else:
        log.logger_LPP.error('Handling on Error messages')
    return lpp_gen.generate_lpp_abort('undefined')


# HANDLER OF ABORT
def handle_abort(body):

    if body['criticalExtensions'][0] == 'c1':
        message_body = body['criticalExtensions'][1]
        if message_body[0]== 'abort-r9':
            Abort=message_body[1]
            for items in Abort:
                match items:
                    case 'commonIEsAbort':
                        log.logger_LPP.warning('ABORT')
                    case 'commonIEsAbort':
                        log.logger_LPP.warning(f'Received this abort: {Abort[items]["abortCause"]}')
                    case 'epdu-Abort':
                        log.logger_LPP.warning(f'Received this abort on {items}')
                    case _:
                        log.logger_LPP.error('Error on Abort messages')
        else:
            log.logger_LPP.error('Handling on Abort messages')
    else:
        log.logger_LPP.error('Handling on Abort messages')

    result= 'abort'
    return result


def handleLPP(lpp_message_asn):
    endFlag = False
    abortFlag = False
    log.logger_LPP.info('Start handling a LPP message')
    lpp_message = decodeLPP(lpp_message_asn)
    
    if lpp_message is None:
        return "ERROR"

    log.logger_LPP.debug(f"------------ lpp_message: {lpp_message}")

    if 'acknowledgement' in lpp_message:
        acknowledgement= lpp_message['acknowledgement']
        if acknowledgement['ackRequested']:
            log.logger_LPP.info(f'ACK Requested for this LPP messages')
        else:
            log.logger_LPP.info(f'ACK NOT Requested for this LPP messages')
        if 'ackIndicator' in acknowledgement:
            log.logger_LPP.info(f'Received the ACK for the SN {acknowledgement["ackIndicator"]}')
        
        fields = ['transactionID', 'endTransaction','sequenceNumber', 'lpp-MessageBody']
        if not all(field in lpp_message for field in fields):
            log.logger_LPP.info(f'Received only the ACK')
            return "OK"
    else:
        fields = ['transactionID', 'endTransaction','sequenceNumber', 'lpp-MessageBody']
        if not all(field in lpp_message for field in fields):
            log.logger_LPP.error(f'Missing fields in LPP messages')
            return "ERROR"

    transaction_idR = lpp_message['transactionID']
    replay_sequence_number = lpp_message['sequenceNumber']
    acknowledgement= lpp_message['acknowledgement']
    end_transactionR = lpp_message['endTransaction']
    ack_requested=acknowledgement['ackRequested']
    
    lmf_instance = lmf.Lmf().get(transaction_idR['transactionNumber'])
    
    if replay_sequence_number in lmf_instance.sequence_number_list:
        log.logger_LPP.warning(f'The LPP messages related to the sequence number {replay_sequence_number} is already received')
        return
    else:
        log.logger_LPP.debug(f'Sequence number {replay_sequence_number} added to the list of received sequence number')
        lmf_instance.update_SN_received(replay_sequence_number)


    log.logger_LPP.debug(f"LPP transaction id: {transaction_idR}")
    log.logger_LPP.debug(f'LPP Request Sequence Number:{replay_sequence_number}')
    log.logger_LPP.debug(f'LPP transaction id:{transaction_idR}')
    log.logger_LPP.debug(f'LPP end transaction:{end_transactionR}')



    #chek the lpp message body
    if 'lpp-MessageBody' in lpp_message:
        lpp_message_body = lpp_message['lpp-MessageBody'][0]

        if lpp_message['lpp-MessageBody'][0] == 'c1':
            lpp_message_body = lpp_message['lpp-MessageBody'][1]
            first_key= lpp_message_body[0]
            first_value= lpp_message_body[1]
            log.logger_LPP.debug(f'LPP Message Body Type: {first_key}')
            log.logger_LPP.debug(f'LPP Message Body Value: {first_value}')
          
            match first_key:
                case 'requestCapabilities':
                    log.logger_LPP.error(f'This type of message {first_key} is not possible to receive')
                    ResponseLPP_Message_body= lpp_gen.generate_lpp_error("incorrectDataValue")
                    endTransaction=True

                case 'provideCapabilities':
                    log.logger_LPP.info(f'Handling {first_key} type of LPP message')
                    try:
                        mode_method_supported = handle_provide_capabilities(first_value)
                    except:
                        log.logger_LPP.error('Error during handle_provide_capabilities function')
                        ResponseLPP_Message_body= lpp_gen.generate_lpp_error("undefined")
                        endTransaction=True
                    
                    # methods_preference from the DB
                    methods_preference=lmf_instance.method_preference

                    for method in methods_preference:
                        for i in mode_method_supported:
                            if method in i['method']:
                                mode_method_selected = {'mode': i['mode'][0], 'method': method }
                                break
                            else:
                                mode_method_selected = {'mode': 'error', 'method': 'error'}
                        if mode_method_selected["mode"] != "error":
                            break                            

                    log.logger_LPP.info(f'Method select {mode_method_selected["method"]} with mode: {mode_method_selected["mode"]}')
                    lmf_instance.set_method_mode(mode_method_selected)
                    

                     # we take the QoS from the DB
                    QoS = lmf_instance.QoS
                    configuration={'QoS': QoS}

                    if mode_method_selected["mode"]=='error':
                        ResponseLPP_Message_body= lpp_gen.generate_lpp_error("undefined")
                        endTransaction=True
                    elif mode_method_selected["mode"]=='Network-Based':
                        ResponseLPP_Message_body={}
                    else:
                        ResponseLPP_Message_body= lpp_gen.generate_lpp_request_location_request(mode_method_selected['method'],mode_method_selected["mode"],configuration)
                        endTransaction=False

                case 'requestAssistanceData': 
                    log.logger_LPP.info(f'Handling {first_key} type of LPP message')
                    try:
                        assistancedata = handle_request_assistance_data(first_value)
                    except:
                        log.logger_LPP.error('Error during handle_request_assistance_data function')
                        ResponseLPP_Message_body= lpp_gen.generate_lpp_error("undefined")
                        endTransaction=True                  
                    if assistancedata == 'error':
                        log.logger_LPP.error('Error during handle_request_assistance_data function')
                        ResponseLPP_Message_body= lpp_gen.generate_lpp_error("undefined")
                        endTransaction=True
                    else:
                        ResponseLPP_Message_body=assistancedata
                        endTransaction=True

                case 'provideAssistanceData': 
                    log.logger_LPP.error(f'This type of message {first_key} is not possible to receive')
                    ResponseLPP_Message_body= lpp_gen.generate_lpp_error("incorrectDataValue")
                    endTransaction=True

                case 'requestLocationInformation':
                    log.logger_LPP.error(f'This type of message {first_key} is not possible to receive')
                    ResponseLPP_Message_body= lpp_gen.generate_lpp_error("incorrectDataValue")
                    endTransaction=True

                case 'provideLocationInformation':
                    log.logger_LPP.info(f'Handling {first_key} type of LPP message')

                    try:
                        result = handle_provide_location_information(first_value)
                    except:
                        log.logger_LPP.error('Error during handle_provide_location_information function')
                        ResponseLPP_Message_body= lpp_gen.generate_lpp_error("undefined")
                        endTransaction=True    

                    if result== 'error':
                        ResponseLPP_Message_body = lpp_gen.generate_lpp_error("undefined")
                        endTransaction=True
                    else:
                        endFlag=True
                case 'abort':
                    log.logger_LPP.info(f'Handling {first_key} type of LPP message')
                    try:
                        handle_abort(first_value)
                    except:
                        log.logger_LPP.error('Error during handle_abort function')                                            
                    abortFlag=True
                    endTransaction=True

                case 'error':
                    log.logger_LPP.info(f'Handling {first_key} type of LPP message')
                    try:
                        ResponseLPP_Message_body = handle_error(first_value)
                    except:
                        log.logger_LPP.error('Error during handle_error function')
                        abortFlag=True
                    endTransaction=True

                case 'spare7', 'spare6', 'spare5', 'spare4', 'spare3', 'spare2', 'spare1', 'spare0':
                    ResponseLPP_Message_body= lpp_gen.generate_lpp_error("incorrectDataValue")
                    endTransaction=True
                    pass
                case _:
                    log.logger_LPP.error(f'This type of message {first_key} is not possible to receive')
                    ResponseLPP_Message_body= lpp_gen.generate_lpp_error("incorrectDataValue")
                    endTransaction=True

        else: 
            log.logger_LPP.error('Error on the structure of LPP message')
            ResponseLPP_Message_body = lpp_gen.generate_lpp_error("incorrectDataValue")
            endTransaction=True
    else:
        log.logger_LPP.error('Missing the LPP message body')
        ResponseLPP_Message_body = lpp_gen.generate_lpp_error("incorrectDataValue")
        endTransaction=True
    

    if abortFlag==True:
        log.logger_LPP.warning('END ESTIMATION PROCESS DUE TO ABORT PROCEDURE')
        if ack_requested:
            ack_sequence_number = replay_sequence_number
            lmf_instance.sequence_number += 1
            LPP_MESSAGE= lpp_gen.generate_LPP__with_ACK(transaction_idR['transactionNumber'], end_transactionR, lmf_instance.sequence_number, ack_sequence_number)
            LPP_MESSAGE_ENCODED= encodeLPP(LPP_MESSAGE)
            log.logger_LPP.debug(f"LPP_Handler - sequence_number: {lmf_instance.sequence_number}")
            lmf.send_message(LPP_MESSAGE_ENCODED, proto="5gnas", imsi=lmf_instance.imsi,lcs_correlation=lmf_instance.lcs_corr_id)  
        # send the notify to the thread that respond to the initial HTTP request with error
        lmf.estimation_procedure_error({'transaction_number': transaction_idR["transactionNumber"]})
        return "ABORT"
    
    if endFlag== True:
        if ack_requested:
            ack_sequence_number = replay_sequence_number
            lmf_instance.sequence_number += 1
            LPP_MESSAGE= lpp_gen.generate_LPP__with_ACK(transaction_idR['transactionNumber'], end_transactionR, lmf_instance.sequence_number, ack_sequence_number)
            LPP_MESSAGE_ENCODED= encodeLPP(LPP_MESSAGE)
            log.logger_LPP.debug(f"LPP_Handler - sequence_number: {lmf_instance.sequence_number}")
            lmf.send_message(LPP_MESSAGE_ENCODED, proto="5gnas", imsi=lmf_instance.imsi,lcs_correlation=lmf_instance.lcs_corr_id)  
        # the estimation is conclude, send the notify to the thread that respond to the initial HTTP request
        log.logger_LPP.info('END ESTIMATION PROCESS DUE TO ESTIMATION COMPLETE')
        log.logger_LPP.info(f'Estimation position:{result}')
        result.update({'transaction_number': transaction_idR["transactionNumber"]})
        lmf.estimation_procedure_completed(result)
        return "OK"
    
    elif ResponseLPP_Message_body=={}:
        if ack_requested:
            ack_sequence_number = replay_sequence_number
            lmf_instance.sequence_number += 1
            LPP_MESSAGE = lpp_gen.generate_LPP__with_ACK(transaction_idR['transactionNumber'], True, lmf_instance.sequence_number, ack_sequence_number)
            LPP_MESSAGE_ENCODED = encodeLPP(LPP_MESSAGE)
            log.logger_LPP.info(f"LPP_Handler - sequence_number: {lmf_instance.sequence_number}")
            lmf.send_message(LPP_MESSAGE_ENCODED, proto="5gnas", imsi=lmf_instance.imsi,lcs_correlation=lmf_instance.lcs_corr_id)  
        # network based mode, no more lpp messages
        log.logger_LPP.info(f'Network Based mode initiate')
        # generate and send nrrpa message
        # Info to be used in the NRPPa message and fix to the moment
        # TODO -> to be updated with the values from the config file
        RequestedSRSTx = {'resourceType': 'aperiodic','bandwidth':  ('fR1', 'mHz100')}
        UEReportingInfo = {'reportingAmount': 'ma1','reportingInterval': 'none'}
        UE_TEG_Info_Request = 'onDemand'

        NRPPa_MESSAGE_=nrppa_gen.PositioningInformationRequest(transaction_idR["transactionNumber"],RequestedSRSTx,UEReportingInfo,UE_TEG_Info_Request)
        NRPPa_MESSAGE_ENCODED= NRPPa_handler.encodeNRPPa(NRPPa_MESSAGE_)
        lmf.send_message(NRPPa_MESSAGE_ENCODED, proto="ngap", imsi=lmf_instance.imsi)
    else:
        log.logger_LPP.debug(f'ResponseLPP_Message_body: {ResponseLPP_Message_body}')

        if ack_requested:
            ack_sequence_number = replay_sequence_number
            lmf_instance.sequence_number += 1
            LPP_MESSAGE = lpp_gen.generate_LPP__with_ACK(transaction_idR['transactionNumber'], endTransaction, lmf_instance.sequence_number, ack_sequence_number, ResponseLPP_Message_body)
        else:
            lmf_instance.sequence_number += 1
            LPP_MESSAGE = lpp_gen.generate_LPP_MESSAGE(transaction_idR['transactionNumber'], endTransaction, lmf_instance.sequence_number, ResponseLPP_Message_body)
        log.logger_LPP.debug(f"LPP_Handler - sequence_number: {lmf_instance.sequence_number}")
        LPP_MESSAGE_ENCODED = encodeLPP(LPP_MESSAGE)

        if LPP_MESSAGE_ENCODED is None:
            ResponseLPP_Message_body = lpp_gen.generate_lpp_error("undefined")
            LPP_MESSAGE = lpp_gen.generate_LPP__with_ACK(transaction_idR['transactionNumber'], endTransaction, lmf_instance.sequence_number, ack_sequence_number, ResponseLPP_Message_body)
            LPP_MESSAGE_ENCODED = encodeLPP(LPP_MESSAGE)
        lmf.send_message(LPP_MESSAGE_ENCODED, proto="5gnas", imsi=lmf_instance.imsi,lcs_correlation=lmf_instance.lcs_corr_id)  
    return "OK"
