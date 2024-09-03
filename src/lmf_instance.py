import requests
import uuid
import config as config
import threading
from threading import Thread, Event
import time
import LPP_message_gen as lpp_gen
from pycrate_asn1dir import LPP
import json
from datetime import datetime, timezone, timedelta
import custom_log as log
import random




LPP_JSON = {
    "n1MessageContainer": {
        "n1MessageClass": "LPP",
        "n1MessageContent": { "contentId": "5gnas"},
        "nfId": config.nfID, 
        "serviceInstanceId": "LMF"
    },
    "lcsCorrelationId": "string",
}
NRPPa_JSON = {
        "n2InfoContainer": {
            "n2InformationClass": "NRPPa",
            "nrppaInfo": {
            "nfId":config.nfID,
            "nrppaPdu": {
                "ngapIeType":"NRPPA_PDU",
                "ngapData":{"contentId": "ngap"}
            },
            "serviceInstanceId": "LMF"
            },
        }
        }
NRPPa_JSON_NON_UE = {
            "taiList": [{
                "plmnId": {
                    "mcc": config.mcc,
                    "mnc": config.mnc
                },
                "tac": config.tac,
            }],
            "ratSelector": "NR",
            "globalRanNodeList": [{
                "plmnId": {
                    "mcc": config.mcc,
                    "mnc": config.mnc
                },
                "gNbId": {
                    "bitLength": config.gNB_bitLength,
                    "gNBValue": config.gNBValue
                }
            }],
            "n2Information": {
                "n2InformationClass": "NRPPa",
                "nrppaInfo": {
                    "nfId": config.nfID,
                    "nrppaPdu": {
                        "ngapIeType": "NRPPA_PDU",
                        "ngapData": {"contentId": "ngap"}
                    },
                    "serviceInstanceId": "LMF"
                }
            }
        }

LMF_DB = dict()

# Contains the localization information of already computed users
# The values are dictionaries with localization information
# It is indexed by IMSI/SUPI/ID
# There is no event to wait for, because only one process at a time (transaction_ID and consequently IMSI) uses it
LMF_POSITION_DB = dict()




# Contains the localization information of a user during computation
# The values are instances of the Lmf() class that contain the event to wait for
# It is a dictionary indexed by transaction_number
# I have the event to wait for
LMF_COMPUTING_DB = dict()


# Check if the position data is valid
# and if the localization status is "finded"
# Return an instance of Lmf() if the data is valid, otherwise return None
def position_is_computing(id):
    ue = LMF_POSITION_DB[id]
    if ue["localisation_status"] == "computing":
        return LMF_COMPUTING_DB[ue["transaction_number"]]
    else:
        return None


# Check if the position data is valid
# and if the localization status is "finded"
def data_is_valid(id):
    try:
        ue = LMF_POSITION_DB[id]
        log.logger_LMF_istance.debug(f'UE status: {ue["localisation_status"]}')
        if ue["localisation_status"] == "finded":
            position_timestamp = datetime.strptime(ue["position_info"]["timestampOfLocationEstimate"], "%Y-%m-%dT%H:%M:%S.%fZ")
            current_datetime = datetime.now(timezone.utc)
            current_datetime = current_datetime.replace(tzinfo=None)
            diff = current_datetime - position_timestamp
            delta = timedelta(seconds=(60*config.MaxAgeOfEstimation)) 
            log.logger_LMF_istance.debug(f'Age of the estimation: {diff}')
            log.logger_LMF_istance.debug(f'Age of the estimation threshold : {delta}')

            if diff < delta:
                log.logger_LMF_istance.debug(f"Valid data for id user: {id}")
                return True
    
    except Exception as err:
        log.logger_LMF_istance.error(f"ERROR: [data_is_valid]: {err}")
        return False
    
    return False

class Lmf():
    
    nfID = config.nfID
    amf_ip = config.AMF_IP
    amf_port = config.AMF_PORT
    lmf_ip = config.LMF_IP
    lmf_port = config.LMF_PORT

    def create(self, jdata, _transaction_number,method_preference):
        self.jdata = jdata
        self.transaction_number = _transaction_number
        self.event = Event()
        self.lcs_corr_id = jdata['correlationID']
        self.sequence_number = 1
        self.method_preference = method_preference 
        self.sequence_number_list = []
        self.NRPPa_measurements = []

        if  jdata['locationQoS']['responseTime'] == 'LOW_DELAY':
            self.QoS =  {'horizontalAccuracy': {'accuracy': jdata['locationQoS']['hAccuracy'], 'confidence': jdata['locationQoS']['hAccuracy']}, 'responseTime': {'time': 5, 'responseTimeEarlyFix-r12': 5}, 'velocityRequest': False, 'verticalCoordinateRequest':  jdata['locationQoS']['verticalRequested']} 
        else: ## DELAY_TOLERANT
            self.QoS =  {'horizontalAccuracy': {'accuracy': jdata['locationQoS']['hAccuracy'], 'confidence': jdata['locationQoS']['hAccuracy']}, 'responseTime': {'time': 15, 'responseTimeEarlyFix-r12': 15}, 'velocityRequest': False, 'verticalCoordinateRequest':  jdata['locationQoS']['verticalRequested']} 

        # Extract the user's ID
        try:
            if "supi" in jdata:
                self.imsi = jdata['supi']
            elif "imsi" in jdata:
                self.imsi = jdata['imsi']
            elif "id" in jdata:
                self.imsi = jdata['id']
            else:
                raise KeyError("supi or imsi or id")
        except KeyError as err:  
            log.logger_LMF_istance.error(f"KeyError: {err} not found")
            exit()
        except Exception as err:
            log.logger_LMF_istance.error(f"Error: {err}")
            exit()
        
        # Create an entry in LMF_POSITION_DB where I will store the localization result.
        # The event to wait for is in the computing DB indexed by transaction_number,
        # which I can retrieve from this DB when the status is computing.
        if 'ldrReference' in jdata.keys():
            LMF_POSITION_DB[self.imsi] = {"localisation_status": "computing", 
                                      "transaction_number": _transaction_number,
                                      "ldr_reference": jdata['ldrReference']}
        else:
            LMF_POSITION_DB[self.imsi] = {"localisation_status": "computing", 
                                      "transaction_number": _transaction_number}

        # Insert entry into the DB where I store the UE in the computing phase
        LMF_COMPUTING_DB[_transaction_number] = self
        
        return self

    def remove_computation_entry(self):
        del LMF_COMPUTING_DB[self.transaction_number]
        
    def get(self, _transaction_number):
        return LMF_COMPUTING_DB[_transaction_number]
        
    def set_location_info(self, position, timestamp, periodic = False):
        ue = LMF_POSITION_DB[self.imsi]
        ue["localisation_status"] = "finded"
        ue["position_info"] = position
        ue["position_timestamp"] = timestamp
        if not periodic:
            ue["transaction_number"] = -1

    def set_error(self, errors):
        ue = LMF_POSITION_DB[self.imsi]
        ue["localisation_status"] = errors
        ue["transaction_number"] = -1
        
    def set_method_mode(self, mode_method_selected):
        self.mode_method=mode_method_selected

    def wait_event(self, max_time=None):
        if max_time:
            self.event.wait(max_time)
        else:
            self.event.wait()

    def update_SN_received(self, sequence_numer):
        self.sequence_number_list.append(sequence_numer)

    def set_event(self):
        self.event.set()
    
    def get_event_status(self):
        return self.event.is_set()
    
    def clear_event(self):
        self.event.clear()
    
    def Add_NRPPa_measurement(self, meas):
        if isinstance(meas,list):
            self.NRPPa_measurements += meas
        else:
            self.NRPPa_measurements.append(meas)


    def subscribe_N1N2(self):
        N1N2_SUBSCRIBE_JSON = {
            "n2InformationClass": "NRPPa",
            "n2NotifyCallbackUri": f"http://{self.lmf_ip}:{self.lmf_port}/nlmf/notifyN2",
            "n1MessageClass": "LPP",
            "n1NotifyCallbackUri": f"http://{self.lmf_ip}:{self.lmf_port}/nlmf/notifyN1",
            "nfId": self.nfID
        }
        # Subscribe to N1/N2 messages
        _url = f"http://{self.amf_ip}:{self.amf_port}/namf-comm/v1/ue-contexts/imsi-{self.imsi}/n1-n2-messages/subscriptions"
                
        try:
            request = requests.post(_url, json=N1N2_SUBSCRIBE_JSON)
            log.logger_LMF_istance.info(f"request.text: {request.text}")
            if request.status_code != 200 and request.status_code != 201:
                raise Exception("N1N2 subscription failed")
            log.logger_LMF_istance.info(f"N1N2 subscription successfully complete")
        except Exception as e:
            log.logger_LMF_istance.error(f"ERROR: [subscribeN1N2] - {e}")
            return
            
        return request.status_code

    def unsubscribe_N1N2(self, subscription_id):
        _url = f"http://{self.amf_ip}:{self.amf_port}/namf-comm/v1/ue-contexts/imsi-{self.imsi}/n1-n2-messages/subscriptions/n1n2NotifySubscriptionId"
        
        try:
            request = requests.delete(_url)
            log.logger_LMF_istance.info(f"request.text: {request.text}")
            if request.status_code != 200 and request.status_code != 204:
                raise Exception("N1N2 unsubscription failed")
            log.logger_LMF_istance.info(f"N1N2 unsubscription successfully complete")
        except Exception as e:
            log.logger_LMF_istance.error(f"ERROR: [unsubscribeN1N2] - {e}")
        return request.status_code


    def subscribe_N2_NonUEAssociated(self):
        N1N2_SUBSCRIBE_JSON = {
            "anTypeList": ["3GPP_ACCESS"],
            "n2InformationClass": "NRPPa",
            "n2NotifyCallbackUri": f"http://{self.lmf_ip}:{self.lmf_port}/nlmf/notifyN2",
            "nfId": f"{uuid.uuid4()}"
        }

        # Subscribe to N2 messages Non UE Associated
        _url = f"http://{self.amf_ip}:{self.amf_port}/namf-comm/v1/non-ue-n2-messages/subscriptions" 
        try:
            request = requests.post(_url, json=N1N2_SUBSCRIBE_JSON)
            log.logger_LMF_istance.info(f"request.text: {request.text}")
            if request.status_code != 200 and request.status_code != 201:
                raise Exception("N1N2 subscription failed")
            log.logger_LMF_istance.info(f"N1N2 Non UE Associated subscription OK")
        except Exception as e:
            log.logger_LMF_istance.error(f"ERROR: [subscribeN1N2] - {e}")
            return
        return request.status_code

    def cancel_location(self):
        pass


def send_nonUEassociated(_encoded_message):
    _url = f"http://{config.AMF_IP}:{config.AMF_PORT}/namf-comm/v1/non-ue-n2-messages/transfer"
    boundary = str(uuid.uuid4())
    content_type = "multipart/related; boundary=" + boundary
    json_message = json.dumps(NRPPa_JSON_NON_UE)
    protoBinary= b'Content-Type: application/vnd.3gpp.ngap'
    content_id = b"Content-Id: ngap"
    
    start_boundary = b"--" + boundary.encode()
    line_separator = b"\r\n"
    body_json = start_boundary + line_separator + b"Content-Type: application/json" + line_separator + line_separator + json_message.encode() + line_separator
    body = start_boundary + line_separator + protoBinary + line_separator +content_id + line_separator + line_separator + _encoded_message + line_separator
    whole_message = body_json + body + start_boundary + b"--" + line_separator

    log.logger_LMF_istance.debug(f'HTTP message:')
    log.logger_LMF_istance.debug(whole_message)
    log.logger_LMF_istance.debug(f'END HTTP message:')
    log.logger_LMF_istance.info(f'NNN UE ASSOCIATED HTTP message send to {_url}')
    response = requests.post(_url, headers={"Content-Type": content_type}, data=whole_message)
    log.logger_LMF_istance.debug(f"Response: {response}")
    
    return response




def send_message(_encoded_message, proto, imsi,lcs_correlation=None, host=None, port=None):
    _url = f"http://{config.AMF_IP}:{config.AMF_PORT}/namf-comm/v1/ue-contexts/imsi-{imsi}/n1-n2-messages"
    boundary = str(uuid.uuid4())
    content_type = "multipart/related; boundary=" + boundary
    
    try:
        if proto == "5gnas":
            LPP_JSON['lcsCorrelationId']=lcs_correlation
            json_message = json.dumps(LPP_JSON)
            protoBinary= b'Content-Type: application/vnd.3gpp.5gnas'
            content_id = b"Content-Id: 5gnas"
        elif proto == "ngap":
            json_message = json.dumps(NRPPa_JSON)
            protoBinary= b'Content-Type: application/vnd.3gpp.ngap'
            content_id = b"Content-Id: ngap"
        else:
            raise Exception("Protocol not supported")

        
        
        log.logger_LMF_istance.debug(f"boundary: {boundary}")
        log.logger_LMF_istance.debug(f"json_message: {json_message}")
        log.logger_LMF_istance.debug(f"content_id: {content_id}")
        log.logger_LMF_istance.debug(f"_encoded_message: {_encoded_message}")
        log.logger_LMF_istance.debug(f"protoBinary: {protoBinary}")


        start_boundary = b"--" + boundary.encode()
        line_separator = b"\r\n"
        body_json = start_boundary + line_separator + b"Content-Type: application/json" + line_separator + line_separator + json_message.encode() + line_separator
        body = start_boundary + line_separator + protoBinary + line_separator +content_id + line_separator + line_separator + _encoded_message + line_separator
        whole_message = body_json + body + start_boundary + b"--" + line_separator

        log.logger_LMF_istance.debug(f'HTTP message:')
        log.logger_LMF_istance.debug(whole_message)
        log.logger_LMF_istance.debug(f'END HTTP message:')
        log.logger_LMF_istance.info(f'HTTP message send to {_url}')
        response = requests.post(_url, headers={"Content-Type": content_type}, data=whole_message)
        log.logger_LMF_istance.debug(f"Response: {response}")
        return response
    
    except Exception as err:
        log.logger_LMF_istance.error(f"ERROR: [send_message]: {err}")
        return



def cancel_location(ldr_reference):

    # check if there is an ongion proecure related to the ldr_reference

    log.logger_LMF_istance.info("\n##CANCEL LOCATION SERVICES##\n")


    for ue_entries in LMF_POSITION_DB.values():
        log.logger_LMF_istance.info(f"ue_entries ---> {ue_entries}")

        if not ('ldr_reference' in ue_entries.keys()):
            return "ERROR"
        
        log.logger_LMF_istance.info("there is the ldrReference field")

        if ue_entries["ldr_reference"] == ldr_reference:  # if there is an procedure related to the ldr_reference
            log.logger_LMF_istance.info("ldr finded")
            if ue_entries['localisation_status'] == 'computing': # if the procedure is ongoing
                
                transaction_number = ue_entries["transaction_number"]
                lmf_istance_to_cancel = Lmf().get(transaction_number)
                
                
                # cancel the ongoing procedure by sending an LPP abort messages to the UE and reply to the AMF with an ERROR 
                log.logger_LMF_istance.info(f"The Location Requested related to the LDR reference {ldr_reference} is cancelled")
                lmf_istance_to_cancel.sequence_number += 1
                lpp_msg_body = lpp_gen.generate_lpp_abort("undefined")
                full_lpp_msg = lpp_gen.generate_LPP_MESSAGE(transaction_number=transaction_number, end_transaction=True, sequence_number=lmf_istance_to_cancel.sequence_number, lpp_message_body=lpp_msg_body)

                M = LPP.LPP_PDU_Definitions.LPP_Message
                M.set_val(full_lpp_msg)
                encoded_msg = M.to_uper()
                log.logger_LMF_istance.debug(f"Encoded_msg_type: {type(encoded_msg)}\nEncoded_msg: {encoded_msg}")

                try:
                    r = send_message(_encoded_message=encoded_msg, proto="5gnas", imsi=lmf_istance_to_cancel.imsi,lcs_correlation=lmf_istance_to_cancel.lcs_corr_id)
                except Exception as e:
                    log.logger_LMF_istance.error(f"ERROR: [send_message]: {e}")
                    exit()

                log.logger_LMF_istance.warning("-------- Start estimation_procedure_error --------")
                # send the error to the initial location request 
                lmf_istance_to_cancel.set_error("cancelled")
                log.logger_LMF_istance.warning(f"NOTIFY - Thread: {threading.get_ident()} - Devo sbloccare evento: {lmf_istance_to_cancel.event} - Stato: {lmf_istance_to_cancel.get_event_status()}")    
                lmf_istance_to_cancel.set_event()
                log.logger_LMF_istance.warning(f"NOTIFY - Thread: {threading.get_ident()} - Ho sbloccato l'evento: {lmf_istance_to_cancel.event} - Stato: {lmf_istance_to_cancel.get_event_status()}")
                return "OK"
            else:
                log.logger_LMF_istance.error(f"The Location Requested related to the LDR reference {ldr_reference} is not ongoing at the moment")
                return "ERROR"

    return "ERROR"        

        




def determine_location_NO_DELAY(jdata):
    log.logger_LMF_istance.info('-------- Start determine_location with NO DELAY --------"')
    
    ue_id = jdata['supi']  
    if ue_id in LMF_POSITION_DB:
        log.logger_LMF_istance.info(f"User data {ue_id} already present in the DB and still valid")
        ue = LMF_POSITION_DB[ue_id]
        result_json = ue["position_info"]
        result_json.update(ue["position_timestamp"])
    else:
        result_json= 'ERROR'
    return result_json


def determine_location(jdata, requested_methods, methods_preference, thread_num=11):
    log.logger_LMF_istance.info('-------- Start determine_location --------"')
    
    ue_id = jdata['supi']
    
    # Localization data present in the DB: LMF_POSITION_DB
    if ue_id in LMF_POSITION_DB:
        # If the data is valid, return it
        if data_is_valid(ue_id):
            log.logger_LMF_istance.info(f"User data {ue_id} already present in the DB and still valid")
            ue = LMF_POSITION_DB[ue_id]
            result_json = ue["position_info"]
            result_json.update(ue["position_timestamp"])
            return result_json
        
        # Someone has requested localization but hasn't finished yet, wait
        # I block in waiting on an event
        lmf = position_is_computing(ue_id)
        if lmf:
            log.logger_LMF_istance.info(f"User position: {ue_id} already requested, waiting for computation to finish")
            start_new_localisation = False
            lmf.wait_event()
        else:
            start_new_localisation = True
    # It's a new request, I need to start the localization procedure
    else:
        start_new_localisation = True
        
    
    if start_new_localisation:
        # Generate a transaction_number

        transaction_number = random.randint(0, 255)
        
        # Check if the transaction_number has already been used
        while transaction_number in LMF_COMPUTING_DB.keys():
            # If I have used all transaction_numbers, wait for 10 seconds
            if len(LMF_COMPUTING_DB) == 255:
                time.sleep(10)
            transaction_number = random.randint(0, 255)
        log.logger_LMF_istance.info(f"Data received in user request: {jdata}")
        
        # Now I obtain an lmf variable useful to start the localization procedure
        lmf = Lmf().create(jdata, transaction_number, methods_preference)
        
        # Subscribe to N1/N2 messages
        lmf.subscribe_N1N2()
        lmf.subscribe_N2_NonUEAssociated() 
        

        # ---------- send LPP RequestCabailities message and wait for N1/N2 message ----------
        # Generate the body of the LPP message    
        lpp_msg_body = lpp_gen.generate_lpp_request_capabilities(requested_methods)
        full_lpp_msg = lpp_gen.generate_LPP_MESSAGE(transaction_number=transaction_number, end_transaction=False, sequence_number=lmf.sequence_number, lpp_message_body=lpp_msg_body)
        # Create and encode the LPP message
        M = LPP.LPP_PDU_Definitions.LPP_Message
        M.set_val(full_lpp_msg)
        encoded_msg = M.to_uper()
        log.logger_LMF_istance.debug(f"Encoded_msg_type: {type(encoded_msg)}\nEncoded_msg: {encoded_msg}")
        # Create and send the HTTP message
        # ---------- send LPP RequestCabailities message and wait for N1/N2 message ----------
        try:
            r = send_message(_encoded_message=encoded_msg, proto="5gnas", imsi=lmf.imsi, lcs_correlation=lmf.lcs_corr_id)
        except Exception as e:
            log.logger_LMF_istance.error(f"ERROR: [send_message]: {e}")
            exit()
        http_code = r.status_code
        http_body_response = r.text
        
        log.logger_LMF_istance.debug(f"http_body_response: {http_body_response}")
        # ---------- wait for N1/N2 message ----------
        log.logger_LMF_istance.info(f"LOCATION - Thread: {threading.get_ident()} - Waiting for event: {lmf.event} - Status: {lmf.get_event_status()}")
        lmf.wait_event(max_time=60)
        log.logger_LMF_istance.info(f"LOCATION -  Thread: {threading.get_ident()} - Finished waiting for event: {lmf.event} - Status: {lmf.get_event_status()}")
        
        # I am the thread that created the localization request, so I am the only one who reaches here
        lmf.clear_event()
        lmf.remove_computation_entry()
        log.logger_LMF_istance.info(f"LOCATION -  Thread: {threading.get_ident()} - Cleared event: {lmf.event} - Status: {lmf.get_event_status()}")
        
        # END OF NEW LOCALIZATION REQUEST PROCEDURE
        

        ue = LMF_POSITION_DB[ue_id]
        if ue["localisation_status"] == "error" or ue["localisation_status"] == "cancelled":
            return "ERROR"
        
        if ue["localisation_status"] == "computing":
            lmf.set_error("error")
            lmf.set_event()
            log.logger_LMF_istance.error(f"Positioning Failed - Timeout Error")
            return "ERROR"
        

        result_json = ue["position_info"]
        result_json.update(ue["position_timestamp"])
        return result_json
        
        
        # The thread that receives the notify and calculates the position inserts it into the lmf object
        # The lmf.position variable will be updated, so I send it as a response
        # return lmf.position
        # END

def estimation_procedure_error(jdata):
    log.logger_LMF_istance.warning("-------- Start estimation_procedure_error --------")
    lmf = Lmf().get(jdata['transaction_number'])
    lmf.set_error("error")

    log.logger_LMF_istance.warning(f"NOTIFY - Thread: {threading.get_ident()} - I need to unlock event: {lmf.event} - Status: {lmf.get_event_status()}")    
    lmf.set_event()
    log.logger_LMF_istance.warning(f"NOTIFY - Thread: {threading.get_ident()} - I have unlocked the event: {lmf.event} - Status: {lmf.get_event_status()}")


def estimation_procedure_completed(jdata, thread_num=22):
    log.logger_LMF_istance.info("-------- Start estimation_procedure_completed --------")
    log.logger_LMF_istance.debug(f"jdata: {jdata}")
    lmf = Lmf().get(jdata['transaction_number'])
    
    if 'timestampOfLocationEstimate' not in jdata:
        estimation_procedure_error(jdata)
        return
        
    timeStamp = {'timestampOfLocationEstimate': jdata['timestampOfLocationEstimate']}
    position = {'locationEstimate': jdata['locationEstimate'] }
    lmf.set_location_info(position,timeStamp)
    
    log.logger_LMF_istance.info(f"NOTIFY - Thread: {threading.get_ident()} - I need to unlock event: {lmf.event} - Status: {lmf.get_event_status()}")    
    lmf.set_event()
    log.logger_LMF_istance.info(f"NOTIFY - Thread: {threading.get_ident()} -I have unlocked the event: {lmf.event} - Status: {lmf.get_event_status()}")
