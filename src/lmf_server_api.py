import sys
import os
sys.path.append(f"{os.path.dirname(sys.path[0])}")

from flask import Flask, request, jsonify
import json
import threading
import custom_log as log
from LPP_message_gen import *
from LPP_handler import *
from NRPPa_handler import *

active_requests = dict()

app = Flask(__name__)



def handle_multipart_related(headerCont, msg):
    try:
        separator = b'--' + (headerCont.replace('"', '').split('boundary=')[1]).encode()
        split_data = msg.split(separator)[1:-1]
        for part in split_data:
            part_divided=part.split(b'\r\n')
            if b'Content-Type: application/json' in part_divided:
                log.logger_LMF_API.info('Handled a JSON body')
                json_body = json.loads(part_divided[3])
                log.logger_LMF_API.debug(f'JSON body: {json_body}')
                
            if b'Content-Type: application/vnd.3gpp.5gnas' in part_divided:
                log.logger_LMF_API.info('Handled a 5gnas body (N1 message)')
                Content_id_Json= json_body["n1MessageContainer"]["n1MessageContent"]["contentId"]
                if f'Content-Id: {Content_id_Json}'.encode() in part_divided:
                    body=part_divided[4]
                    log.logger_LMF_API.debug('Binary body (LPP): {body}')
                    #handle the LPP message 
                    handleLPP(body) 
                else:
                    log.logger_LMF_API.warning('Content-Id in the multipart body not equal in the Json Body')
                    body=part_divided[4]
                    log.logger_LMF_API.debug(f'Binary body (LPP): {body}')
                    #handle the LPP message 
                    handleLPP(body) 

            if b'Content-Type: application/vnd.3gpp.ngap' in part_divided:
                log.logger_LMF_API.info('Handled a NGAP body (N2 message)')
                Content_id_Json= json_body["n2InfoContainer"]["nrppaInfo"]["nrppaPdu"]["ngapData"]["contentId"]
                if f'Content-Id: {Content_id_Json}'.encode() in part_divided:
                    body=part_divided[4]
                    log.logger_LMF_API.debug('Binary body (NRPPa): {body}')
                    #handle the NRPPa message 
                    handlerNRPPa(body)
                else:
                    log.logger_LMF_API.warning('Content-Id in the multipart body not equal in the Json Body')
                    body=part_divided[4]
                    log.logger_LMF_API.debug('Binary body (NRPPa): {body}')
                    #handle the NRPPa message 
                    handlerNRPPa(body)
                    
    except Exception as err:
        log.logger_LMF_API.error(f'ERROR in handle_multipart_related-> {err}')
        return "ERROR"
        

def handle_QoS(jdata):

    repsonseTime= jdata['locationQoS']['responseTime']
    lcsQosClass= jdata['locationQoS']['lcsQosClass']
    if jdata['locationQoS']['verticalRequested']: 
        accuracyLoc= {'hAccuracy': jdata['locationQoS']['hAccuracy'],'vAccuracy':jdata['locationQoS']['vAccuracy']}
    else:
        accuracyLoc= {'hAccuracy': jdata['locationQoS']['hAccuracy']}

    log.logger_LMF_API.info(f'## QoS requested for the location request ##')
    log.logger_LMF_API.info(f'Requested responseTime: {repsonseTime}')
    log.logger_LMF_API.info(f'Requested lcsQosClass: {lcsQosClass}')
    log.logger_LMF_API.info(f'Requested accuracyLoc: {accuracyLoc}')


    match repsonseTime:
        case 'NO_DELAY': 
            # check immeditaly if there is already a estimation computed without computed
            ResultJson = lmf.determine_location_NO_DELAY(jdata)
            return ResultJson
        case 'LOW_DELAY':
            methods_preference = ['nr-DL-TDOA', 'nr-Multi-RTT', 'a-gnss', 'nr-DL-AoD', 'nr-ECID', 'otdoa', 'ecid']
            
        case 'DELAY_TOLERANT':
            methods_preference = ['nr-Multi-RTT', 'nr-DL-TDOA', 'a-gnss', 'nr-DL-AoD', 'nr-ECID', 'otdoa', 'ecid']

    match lcsQosClass:
        case 'BEST_EFFORT':
            methodsRequested=['a-gnss-RequestCapabilities','otdoa-RequestCapabilities','ecid-RequestCapabilities','sensor-RequestCapabilities-r13', 'tbs-RequestCapabilities-r13','wlan-RequestCapabilities-r13','bt-RequestCapabilities-r13','nr-ECID-RequestCapabilities-r16','nr-Multi-RTT-RequestCapabilities-r16','nr-DL-AoD-RequestCapabilities-r16','nr-DL-TDOA-RequestCapabilities-r16','nr-UL-RequestCapabilities-r16']
            ResultJson = lmf.determine_location(jdata, requested_methods=methodsRequested, methods_preference=methods_preference)

        case 'ASSURED':
            log.logger_LMF_API.warning(f'{lcsQosClass} QoS class not supported')
            methodsRequested=['a-gnss-RequestCapabilities','otdoa-RequestCapabilities','ecid-RequestCapabilities','sensor-RequestCapabilities-r13', 'tbs-RequestCapabilities-r13','wlan-RequestCapabilities-r13','bt-RequestCapabilities-r13','nr-ECID-RequestCapabilities-r16','nr-Multi-RTT-RequestCapabilities-r16','nr-DL-AoD-RequestCapabilities-r16','nr-DL-TDOA-RequestCapabilities-r16','nr-UL-RequestCapabilities-r16']
            ResultJson = lmf.determine_location(jdata, requested_methods=methodsRequested, methods_preference=methods_preference)
            ResultJson['accuracyFulfilmentIndicator']='REQUESTED_ACCURACY_FULFILLED'
            # Do some check on the accuracy if ok -> send response otherwise error
            if not ResultJson['accuracyFulfilmentIndicator'] == 'REQUESTED_ACCURACY_FULFILLED':
                ResultJson= 'ERROR'

        case 'MULTIPLE_QOS':
            log.logger_LMF_API.warning(f'{lcsQosClass} QoS class not supported')
            ResultJson= 'ERROR'

    return ResultJson


# LMF Location Service Nllmf_Location

@app.route('/nlmf/notifyN1', methods=['POST'])
def handle_http_notifyN1():
    try:
        if not 'multipart/related' in request.headers['Content-Type']:
            log.logger_LMF_API.error('Data is not a multipart/related data')
            error_message = {'cause': 'Nomultipart/related data'}
            error_message_JSON = jsonify(error_message)
            error_message_JSON.status_code = 415
            error_message_JSON.headers['Content-Type'] = 'application/problem+json'
            return error_message_JSON        
        log.logger_LMF_API.info('Received a message in /nlmf/notifyN1')
        log.logger_LMF_API.debug(f"Request in notify: {request}\n")
        headerCont= request.headers.get("Content-Type")
        msg = request.get_data()
        handle_multiparth_thread = threading.Thread(target=handle_multipart_related, args=[headerCont, msg])
        handle_multiparth_thread.start()

        return "", 204
    except Exception as err:
        log.logger_LMF_API.error(f'ERROR in handle_http_notifyN1-> {err}')
        return "", 501   

@app.route('/nlmf/notifyN2', methods=['POST'])
def handle_http_notifyN2():
    try:
        if not 'multipart/related' in request.headers['Content-Type']:
            log.logger_LMF_API.error('Data is not a multipart/related data')
            error_message = {'cause': 'Nomultipart/related data'}
            error_message_JSON = jsonify(error_message)
            error_message_JSON.status_code = 415
            error_message_JSON.headers['Content-Type'] = 'application/problem+json'
            return error_message_JSON        
        
        log.logger_LMF_API.info('Received a message in /nlmf/notifyN2')
        log.logger_LMF_API.debug(f"Request in notify: {request}\n")
        headerCont = request.headers.get("Content-Type")
        msg = request.get_data()
        handle_multiparth_thread = threading.Thread(target=handle_multipart_related, args=[headerCont, msg])
        handle_multiparth_thread.start()
        return "", 204
    except Exception as err:
        log.logger_LMF_API.error(f'ERROR in handle_http_notifyN2-> {err}')
        return "", 501




@app.route('/nlmf-loc/v1/determine-location', methods=['POST'])
def hande_http_determine_location():
    
    if not request.is_json:
        log.logger_LMF_API.error('Data is not a JSON')
        error_message = {'cause': 'No JSON data'}
        error_message_JSON = jsonify(error_message)
        error_message_JSON.status_code = 415
        error_message_JSON.headers['Content-Type'] = 'application/problem+json'
        return error_message_JSON
    try:
        jdata = request.get_json()
    except Exception as err:
        log.logger_LMF_API.error('ERROR -> {err}')
        exit()
        
    
    ResultJson = handle_QoS(jdata)

    if ResultJson == "ERROR":
        log.logger_LMF_API.error('POSITIONING_FAILED')
        error_message = {'cause': 'POSITIONING_FAILED'}
        error_message_Pos = jsonify(error_message)
        error_message_Pos.status_code = 500
        error_message_Pos.headers['Content-Type'] = 'application/problem+json'
        return error_message_Pos

    if not ResultJson:
        return "ERROR\n", 500

    return jsonify(ResultJson)

@app.route('/nlmf-loc/v1/cancel-location', methods=['POST'])
def hande_http_cancel_location():
    if not request.is_json:
        log.logger_LMF_API.error('Data is not a JSON')
        error_message = {'cause': 'No JSON data'}
        error_message_JSON = jsonify(error_message)
        error_message_JSON.status_code = 415
        error_message_JSON.headers['Content-Type'] = 'application/problem+json'
        return error_message_JSON


    # cancell the ongoing procedure of estimation if it is periodic or triggered (not yet implemented at the moment)
    jdata = request.get_json()
    try:
        hgmlcCallBackURI= jdata['hgmlcCallBackURI']
        ldrReference= jdata['ldrReference']
    except Exception as err:
        log.logger_LMF_API.error(f'Mandatory items not present in the request')
        return "",500
    # check the ldr reference in the db e stop the ongiong procedure
    result = lmf.cancel_location(ldrReference)

    if result== "ERROR":
        log.logger_LMF_API.error('Error during the CancelLocation service')    
        error_message = {'cause': 'LOCATION_SESSION_UNKNOWN'}
        error_message_JSON = jsonify(error_message)
        error_message_JSON.status_code = 403
        error_message_JSON.headers['Content-Type'] = 'application/problem+json'
        return error_message_JSON
    else:
        return "",204

# NOT SUPPORTED --> TODO IN FUTURE VERSION

@app.route('/nlmf-loc/v1/location-context-transfer', methods=['POST'])
def hande_http_location_context_transfer():
    if not request.is_json:
        log.logger_LMF_API.error('Data is not a JSON')    
        error_message = {'cause': 'No JSON data'}
        error_message_JSON = jsonify(error_message)
        error_message_JSON.status_code = 415
        error_message_JSON.headers['Content-Type'] = 'application/problem+json'
        return error_message_JSON
    
    jdata = request.get_json()
    try:
        amfId=jdata['jdata']
        ldrType=jdata['ldrType']
        hgmlcCallBackURI=jdata['hgmlcCallBackURI']
        ldrReference=jdata['ldrReference']
        eventReportMessage=jdata['eventReportMessage']
        #TODO IN FUTURE VERSION
    except Exception as err:
        log.logger_LMF_API.error(f'Mandatory items not present in the request')
        return "",500

    log.logger_LMF_API.warning(f'Services of location-context-transfer not supported')
    return "",500





# LMF LMF Broadcast Service Nlmf_Broadcast

@app.route('/nlmf-broadcast/v1/cipher-key-data', methods=['POST'])
def hande_http_cipher_key_data():
    if not request.is_json:
        log.logger_LMF_API.error('Data is not a JSON')    
        error_message = {'cause': 'No JSON data'}
        error_message_JSON = jsonify(error_message)
        error_message_JSON.status_code = 415
        error_message_JSON.headers['Content-Type'] = 'application/problem+json'
        return error_message_JSON
    
    log.logger_LMF_API.warning(f'Services of location-context-transfer not supported')
    #TODO IN FUTURE VERSION
    return "",500


if __name__ == '__main__':
    app.run(host=config.LMF_IP, port=config.LMF_API_PORT, debug=False)

