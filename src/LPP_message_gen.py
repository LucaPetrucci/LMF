import custom_log as log
import config

# FUNCTIONS FOR GENERATING THE LPP MESSAGES USED BY THE LMF
# GENERATE LPP ABORT MESSAGE
def generate_lpp_abort(type):
    # Type = undefined
    Abort= ("c1", ( "abort", { "criticalExtensions": ( "c1", ("abort-r9", {'commonIEsAbort': {'abortCause': type}}))}))
    return Abort

# GENERATE LPP ERROR MESSAGE
def generate_lpp_error(type):
    Error= ("c1", ( "error", ("error-r9", {'commonIEsError': {'errorCause': type}} )))
    return Error

# GENERATE LPP REQUEST CAPABILITIES FROM THE METHODS
def generate_lpp_request_capabilities(methods):

    RequestCabailities= ("c1", ( "requestCapabilities", { "criticalExtensions": ( "c1", ("requestCapabilities-r9", {}))}))
    checkMethods=['a-gnss-RequestCapabilities','otdoa-RequestCapabilities','ecid-RequestCapabilities','epdu-RequestCapabilities','sensor-RequestCapabilities-r13', 'tbs-RequestCapabilities-r13','wlan-RequestCapabilities-r13','bt-RequestCapabilities-r13','nr-ECID-RequestCapabilities-r16','nr-Multi-RTT-RequestCapabilities-r16','nr-DL-AoD-RequestCapabilities-r16','nr-DL-TDOA-RequestCapabilities-r16','nr-UL-RequestCapabilities-r16']

    commonIE= {'commonIEsRequestCapabilities': {'lpp-message-segmentation-req-r14': (0,2)}}
    RequestCabailities[1][1]['criticalExtensions'][1][1].update(commonIE)
    for item in methods:
        if item in checkMethods:

            if item=='a-gnss-RequestCapabilities':
                new_dict ={item: {'gnss-SupportListReq': True,'assistanceDataSupportListReq':False,'locationVelocityTypesReq':False}}
            else:
                new_dict = {item : {}}
            RequestCabailities[1][1]['criticalExtensions'][1][1].update(new_dict)
        else:    
            log.logger_LPP.error(f"Error during the generating of the request capabilities message - {item}")
            return 'ERROR'
    return RequestCabailities

# GENERATE LPP PROVIDE ASSISTANCE DATA FROM THE METHOD USED
# For the moment the assistance data response is fixed and Multi-RTT and TDOA are supported
# TODO fix the response based on the method and the capabilities of the networks
def generate_lpp_provide_assistance_data(method):

    match method:
        case 'nr-Multi-RTT-RequestAssistanceData-r16':
            AssistanceDataRTT = {
                'nr-DL-PRS-AssistanceData-r16': {
                    'nr-DL-PRS-ReferenceInfo-r16': {
                        'dl-PRS-ID-r16': 11,
                        'nr-DL-PRS-ResourceID-List-r16': [3, 4]
                    },
                    'nr-DL-PRS-AssistanceDataList-r16': [
                        {
                            'nr-DL-PRS-PositioningFrequencyLayer-r16': {
                                'dl-PRS-SubcarrierSpacing-r16': 'kHz15',
                                'dl-PRS-ResourceBandwidth-r16': 45,
                                'dl-PRS-StartPRB-r16': 22,
                                'dl-PRS-PointA-r16': 444,
                                'dl-PRS-CombSizeN-r16': 'n2',
                                'dl-PRS-CyclicPrefix-r16': 'normal'
                            },
                            'nr-DL-PRS-AssistanceDataPerFreq-r16': [
                                {
                                    'dl-PRS-ID-r16': 44,
                                    'nr-PhysCellID-r16': 33,
                                    'nr-CellGlobalID-r16': {
                                        'mcc-r15': [int(config.mcc[0]), int(config.mcc[1]), int(config.mcc[2])],
                                        'mnc-r15': [int(config.mnc[0]), int(config.mnc[1])],
                                        'nr-cellidentity-r15': (5,36) 
                                    },
                                    'nr-ARFCN-r16': 445,
                                    'nr-DL-PRS-SFN0-Offset-r16': {
                                        'sfn-Offset-r16': 44,
                                        'integerSubframeOffset-r16': 5
                                    },
                                    'nr-DL-PRS-ExpectedRSTD-r16': 4,
                                    'nr-DL-PRS-ExpectedRSTD-Uncertainty-r16': 55,
                                    'nr-DL-PRS-Info-r16': {
                                        'nr-DL-PRS-ResourceSetList-r16': [
                                            {
                                                'nr-DL-PRS-ResourceSetID-r16': 4,
                                                'dl-PRS-Periodicity-and-ResourceSetSlotOffset-r16': ('scs30-r16', ('n8-r16', 2)),
                                                'dl-PRS-ResourceRepetitionFactor-r16': 'n2',
                                                'dl-PRS-NumSymbols-r16': 'n2',
                                                'dl-PRS-MutingOption1-r16': {
                                                    'dl-prs-MutingBitRepetitionFactor-r16': 'n2',
                                                    'nr-option1-muting-r16': ('po8-r16', (1,8) )
                                                },
                                                'dl-PRS-MutingOption2-r16': {
                                                    'nr-option2-muting-r16': ('po8-r16', (1,8) )                                                },
                                                'dl-PRS-ResourcePower-r16': 33,
                                                'dl-PRS-ResourceList-r16': [
                                                    {
                                                        'nr-DL-PRS-ResourceID-r16': 4,
                                                        'dl-PRS-SequenceID-r16': 55,
                                                        'dl-PRS-CombSizeN-AndReOffset-r16': ('n2-r16', 1),
                                                        'dl-PRS-ResourceSlotOffset-r16': 2,
                                                        'dl-PRS-ResourceSymbolOffset-r16': 3,
                                                        'dl-PRS-QCL-Info-r16': (
                                                            'dl-PRS-r16', {
                                                                'qcl-DL-PRS-ResourceID-r16': 3,
                                                                'qcl-DL-PRS-ResourceSetID-r16': 4
                                                            }
                                                        )
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    'prs-OnlyTP-r16': 'true'
                                }
                            ]
                        }
                    ],
                    'nr-SSB-Config-r16': [
                        {
                            'nr-PhysCellID-r16': 33,
                            'nr-ARFCN-r16': 445,
                            'ss-PBCH-BlockPower-r16': 44,
                            'halfFrameIndex-r16': 1,
                            'ssb-periodicity-r16': 'ms5',
                            'ssb-PositionsInBurst-r16': ('mediumBitmap-r16', (1,8)),
                            'ssb-SubcarrierSpacing-r16': 'kHz30',
                            'sfn-SSB-Offset-r16': 2
                        }
                    ]
                },
                'nr-SelectedDL-PRS-IndexList-r16': [
                    {
                        'nr-SelectedDL-PRS-FrequencyLayerIndex-r16': 1,
                        'nr-SelectedDL-PRS-IndexListPerFreq-r16': [
                            {
                                'nr-SelectedTRP-Index-r16': 1,
                                'dl-SelectedPRS-ResourceSetIndexList-r16': [
                                    {
                                        'nr-DL-SelectedPRS-ResourceSetIndex-r16': 1,
                                        'dl-SelectedPRS-ResourceIndexList-r16': [
                                            {'nr-DL-SelectedPRS-ResourceIdIndex-r16': 1}
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

            ResponseLPP_Message_body= ("c1", ( "provideAssistanceData", { "criticalExtensions": ( "c1", ("provideAssistanceData-r9", 
                                            {    'nr-Multi-RTT-ProvideAssistanceData-r16': AssistanceDataRTT    }       ))}))
            
        case "nr-DL-TDOA-RequestAssistanceData-r16":
            
            AssistanceDataDLTDOA={
                'nr-DL-PRS-AssistanceData-r16': {
                    'nr-DL-PRS-ReferenceInfo-r16': {
                        'dl-PRS-ID-r16': 11,
                        'nr-DL-PRS-ResourceID-List-r16': [3, 4]
                    },
                    'nr-DL-PRS-AssistanceDataList-r16': [
                        {
                            'nr-DL-PRS-PositioningFrequencyLayer-r16': {
                                'dl-PRS-SubcarrierSpacing-r16': 'kHz30',
                                'dl-PRS-ResourceBandwidth-r16': 45,
                                'dl-PRS-StartPRB-r16': 0,
                                'dl-PRS-PointA-r16': 1,
                                'dl-PRS-CombSizeN-r16': 'n2',
                                'dl-PRS-CyclicPrefix-r16': 'normal'
                            },
                            'nr-DL-PRS-AssistanceDataPerFreq-r16': [
                                {
                                    'dl-PRS-ID-r16': 44,
                                    'nr-PhysCellID-r16': 33,
                                    'nr-CellGlobalID-r16': {
                                        'mcc-r15': [int(config.mcc[0]), int(config.mcc[1]), int(config.mcc[2])],
                                        'mnc-r15': [int(config.mnc[0]), int(config.mnc[1])],
                                        'nr-cellidentity-r15': (5,36) 
                                    },
                                    'nr-ARFCN-r16': 445,
                                    'nr-DL-PRS-SFN0-Offset-r16': {
                                        'sfn-Offset-r16': 44,
                                        'integerSubframeOffset-r16': 5
                                    },
                                    'nr-DL-PRS-ExpectedRSTD-r16': 4,
                                    'nr-DL-PRS-ExpectedRSTD-Uncertainty-r16': 55,
                                    'nr-DL-PRS-Info-r16': {
                                        'nr-DL-PRS-ResourceSetList-r16': [
                                            {
                                                'nr-DL-PRS-ResourceSetID-r16': 4,
                                                'dl-PRS-Periodicity-and-ResourceSetSlotOffset-r16': ('scs30-r16', ('n8-r16', 2)),
                                                'dl-PRS-ResourceRepetitionFactor-r16': 'n2',
                                                'dl-PRS-NumSymbols-r16': 'n2',
                                                'dl-PRS-MutingOption1-r16': {
                                                    'dl-prs-MutingBitRepetitionFactor-r16': 'n2',
                                                    'nr-option1-muting-r16': ('po8-r16', (1,8) )
                                                },
                                                'dl-PRS-MutingOption2-r16': {
                                                    'nr-option2-muting-r16': ('po8-r16', (1,8) )
                                                },
                                                'dl-PRS-ResourcePower-r16': 33,
                                                'dl-PRS-ResourceList-r16': [
                                                    {
                                                        'nr-DL-PRS-ResourceID-r16': 4,
                                                        'dl-PRS-SequenceID-r16': 55,
                                                        'dl-PRS-CombSizeN-AndReOffset-r16': ('n2-r16', 1),
                                                        'dl-PRS-ResourceSlotOffset-r16': 2,
                                                        'dl-PRS-ResourceSymbolOffset-r16': 3,
                                                        'dl-PRS-QCL-Info-r16': (
                                                            'dl-PRS-r16', {
                                                                'qcl-DL-PRS-ResourceID-r16': 3,
                                                                'qcl-DL-PRS-ResourceSetID-r16': 4
                                                            }
                                                        )
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    'prs-OnlyTP-r16': 'true'
                                }
                            ]
                        }
                    ],
                    'nr-SSB-Config-r16': [
                        {
                            'nr-PhysCellID-r16': 33,
                            'nr-ARFCN-r16': 445,
                            'ss-PBCH-BlockPower-r16': 44,
                            'halfFrameIndex-r16': 1,
                            'ssb-periodicity-r16': 'ms5',
                            'ssb-PositionsInBurst-r16': ('mediumBitmap-r16', (1,8)),
                            'ssb-SubcarrierSpacing-r16': 'kHz30',
                            'sfn-SSB-Offset-r16': 2
                        }
                    ]
                },
                'nr-SelectedDL-PRS-IndexList-r16': [
                    {
                        'nr-SelectedDL-PRS-FrequencyLayerIndex-r16': 1,
                        'nr-SelectedDL-PRS-IndexListPerFreq-r16': [
                            {
                                'nr-SelectedTRP-Index-r16': 1,
                                'dl-SelectedPRS-ResourceSetIndexList-r16': [
                                    {
                                        'nr-DL-SelectedPRS-ResourceSetIndex-r16': 1,
                                        'dl-SelectedPRS-ResourceIndexList-r16': [
                                            {'nr-DL-SelectedPRS-ResourceIdIndex-r16': 1}
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

            
            ResponseLPP_Message_body= ("c1", ( "provideAssistanceData", { "criticalExtensions": ( "c1", ("provideAssistanceData-r9", 
                                            {    'nr-DL-TDOA-ProvideAssistanceData-r16': AssistanceDataDLTDOA    }       ))}))            

        case _:
                
                log.logger_LocAlg.error("INTERNAL ERROR Methods non valid ")
                ResponseLPP_Message_body= generate_lpp_error("incorrectDataValue")

    return ResponseLPP_Message_body

# GENERATE LPP REQUEST LOCATION INFORMATION BASED ON METHOD, MODE
def generate_lpp_request_location_request(method,mode,configuration):
    

    QoS= configuration['QoS']

    LocationIEs={}
    match mode:
        case 'UE-Based':
            LocationIEs.update({'commonIEsRequestLocationInformation': {'locationInformationType': 'locationEstimateRequired'},})
        case 'UE-Assisted':
            LocationIEs.update({'commonIEsRequestLocationInformation': {'locationInformationType': 'locationMeasurementsRequired',
                                                                        'triggeredReporting': {'cellChange': True, 'reportingDuration': 0},
                                                                        'segmentationInfo-r14': 'noMoreMessages',
                                                                        'qos': QoS,
                                                                        'environment': 'mixedArea',
                                                                        'messageSizeLimitNB-r14': {'measurementLimit-r14':100},
                                                                        'targetIntegrityRisk-r17': 12,
                                                                        'scheduledLocationTime-r17': {
                                                                            'networkTime-r17': ('nrTime-r17', {
                                                                                'nr-PhysCellID-r17'	:	500,
                                                                                'nr-ARFCN-r17'		:	632628,
                                                                                'nr-CellGlobalID-r17':	{
                                                                                    'mcc-r15': [int(config.mcc[0]), int(config.mcc[1]), int(config.mcc[2])],
                                                                                    'mnc-r15': [int(config.mnc[0]), int(config.mnc[1])],
                                                                                    'nr-cellidentity-r15': (5,36) 
                                                                                                          },
                                                                                'nr-SFN-r17'		:	1,
                                                                                'nr-Slot-r17': ('scs30-r17',1)})
                                                                                }
                                                                                }
                                })
        case 'Standalone':
            LocationIEs.update({'commonIEsRequestLocationInformation': {'locationInformationType': 'locationEstimateRequired',
                                                                        'qos': QoS,
                                                                        'segmentationInfo-r14': 'noMoreMessages',
                                                                        'locationCoordinateTypes': {
                                                                                'ellipsoidPoint': True,
                                                                                'ellipsoidPointWithUncertaintyCircle': True,
                                                                                'ellipsoidPointWithUncertaintyEllipse': True,
                                                                                'polygon': False,
                                                                                'ellipsoidPointWithAltitude': True,
                                                                                'ellipsoidPointWithAltitudeAndUncertaintyEllipsoid': True,
                                                                                'ellipsoidArc': False
                                                                        },
                                                                        "velocityTypes" : {
                                                                                'horizontalVelocity': True,
                                                                                'horizontalWithVerticalVelocity': True,
                                                                                'horizontalVelocityWithUncertainty': True,
                                                                                'horizontalWithVerticalVelocityAndUncertainty': True
                                                                        }
                                                                        }})

    match method:
        case 'a-gnss':
            Val={
                'gnss-Methods': {'gnss-ids': (1,16)}, # GPS requested
                'fineTimeAssistanceMeasReq' : False,
                'adrMeasReq': False,
                'multiFreqMeasReq': False,
                'assistanceAvailability':False }
            LocationIEs.update({'a-gnss-RequestLocationInformation': {'gnss-PositioningInstructions': Val}})
        case 'otdoa':
            LocationIEs.update({'otdoa-RequestLocationInformation': {'assistanceAvailability': False}}) 
        case 'ecid':
            LocationIEs.update({'ecid-RequestLocationInformation': {'requestedMeasurements': (1,4)}})
        case 'sensor':
            log.logger_LocAlg.error(f' NOT SUPPORTED {method} METHOD')
            ResponseLPP_Message_body= generate_lpp_error("incorrectDataValue")
        case 'tbs':
            log.logger_LocAlg.error(f' NOT SUPPORTED {method} METHOD')
            ResponseLPP_Message_body= generate_lpp_error("incorrectDataValue")
        case 'wlan':
            log.logger_LPP.error(f' NOT SUPPORTED {method} METHOD')
            ResponseLPP_Message_body= generate_lpp_error("incorrectDataValue")
        case 'bt':
            log.logger_LPP.error(f' NOT SUPPORTED {method} METHOD')
            ResponseLPP_Message_body= generate_lpp_error("incorrectDataValue")
        case 'nr-ECID':
            LocationIEs.update({'nr-ECID-RequestLocationInformation-r16': {'requestedMeasurements-r16': (1,8)}})
        case 'nr-Multi-RTT':
            LocationIEs.update({'nr-Multi-RTT-RequestLocationInformation-r16': {   
                                                        'nr-UE-RxTxTimeDiffMeasurementInfoRequest-r16': 'true',
                                                        'nr-RequestedMeasurements-r16': (1,8),
                                                        'nr-AssistanceAvailability-r16': True,
                                                        'nr-Multi-RTT-ReportConfig-r16':  {'maxDL-PRS-RxTxTimeDiffMeasPerTRP-r16': 1,'timingReportingGranularityFactor-r16':1}}})                                            
        case 'nr-DL-AoD':
            log.logger_LPP.error(f' NOT SUPPORTED {method} METHOD')
            ResponseLPP_Message_body= generate_lpp_error("incorrectDataValue")
        case 'nr-DL-TDOA':      
            LocationIEs.update({ 'nr-DL-TDOA-RequestLocationInformation-r16': {
                'nr-DL-PRS-RstdMeasurementInfoRequest-r16': 'true',
                'nr-RequestedMeasurements-r16': (0,8),
                'nr-AssistanceAvailability-r16': False
                    }
                    })
        case _:
            log.logger_LPP.error('INTERNAL ERROR Methods non valid ')
            ResponseLPP_Message_body= generate_lpp_error("incorrectDataValue")



    RequestLocationInformation= ("c1", ( "requestLocationInformation", { "criticalExtensions": ( "c1", ("requestLocationInformation-r9", LocationIEs  ))}))
    ResponseLPP_Message_body = RequestLocationInformation
    return ResponseLPP_Message_body    


# FUNCTION TO GENERATE THE WHOLE LPP MESSAGE FROM THE MAIN VALUE
def generate_LPP_MESSAGE(transaction_number, end_transaction, sequence_number, lpp_message_body=None):
    if lpp_message_body==None:
        lpp_msg = {
            "transactionID": {
                "initiator": "locationServer",
                "transactionNumber": transaction_number % 255 
            },
            'acknowledgement':{'ackRequested':True},
            "endTransaction": end_transaction,
            "sequenceNumber": sequence_number  % 255 
        }
    else:
        lpp_msg = {
            "transactionID": {
                "initiator": "locationServer",
                "transactionNumber": transaction_number % 255 
            },
            'acknowledgement':{'ackRequested':True},
            "endTransaction": end_transaction,
            "sequenceNumber": sequence_number  % 255 ,
            "lpp-MessageBody": lpp_message_body
        }
    return lpp_msg

# FUNCTION TO GENERATE THE WHOLE LPP MESSAGE FROM THE MAIN VALUE
def generate_LPP__with_ACK(transaction_number, end_transaction, sequence_number, resp_ACK, lpp_message_body=None):
    
    if lpp_message_body==None:
        lpp_msg = {
            "transactionID": {
                "initiator": "locationServer",
                "transactionNumber": transaction_number % 255 
            },
            'acknowledgement':{'ackRequested': False,'ackIndicator': resp_ACK},
            "endTransaction": end_transaction,
            "sequenceNumber": sequence_number  % 255 ,
        }
    else:
        lpp_msg = {
            "transactionID": {
                "initiator": "locationServer",
                "transactionNumber": transaction_number % 255 
            },
            'acknowledgement':{'ackRequested':True,'ackIndicator':resp_ACK},
            "endTransaction": end_transaction,
            "sequenceNumber": sequence_number  % 255 ,
            "lpp-MessageBody": lpp_message_body

        } 
    return lpp_msg

