# FUNCTIONS FOR GENERATING THE NRPPa MESSAGES USED BY THE LMF


from enum import Enum

## procedure code of the messages NRPPa
class ProcedureCodeEP(Enum):
    id_errorIndication							= 0
    id_privateMessage							= 1
    id_e_CIDMeasurementInitiation			    = 2 
    id_e_CIDMeasurementFailureIndication		= 3 
    id_e_CIDMeasurementReport					= 4 
    id_e_CIDMeasurementTermination				= 5 
    id_oTDOAInformationExchange					= 6 
    id_assistanceInformationControl				= 7 
    id_assistanceInformationFeedback			= 8 
    id_positioningInformationExchange			= 9 
    id_positioningInformationUpdate				= 10 
    id_Measurement								= 11 
    id_MeasurementReport						= 12
    id_MeasurementUpdate						= 13
    id_MeasurementAbort							= 14
    id_MeasurementFailureIndication				= 15
    id_tRPInformationExchange					= 16
    id_positioningActivation					= 17
    id_positioningDeactivation					= 18
    id_pRSConfigurationExchange					= 19
    id_measurementPreconfiguration				= 20
    id_measurementActivation					= 21

class IEs_id(Enum):
    id_Cause														 = 0
    id_CriticalityDiagnostics										 = 1
    id_LMF_UE_Measurement_ID										 = 2
    id_ReportCharacteristics										 = 3
    id_MeasurementPeriodicity										 = 4
    id_MeasurementQuantities										 = 5
    id_RAN_UE_Measurement_ID										 = 6
    id_E_CID_MeasurementResult										 = 7
    id_OTDOACells													 = 8
    id_OTDOA_Information_Type_Group									 = 9
    id_OTDOA_Information_Type_Item									 = 10
    id_MeasurementQuantities_Item									 = 11
    id_RequestedSRSTransmissionCharacteristics						 = 12
    id_Cell_Portion_ID												 = 14
    id_OtherRATMeasurementQuantities								 = 15
    id_OtherRATMeasurementQuantities_Item							 = 16
    id_OtherRATMeasurementResult									 = 17
    id_WLANMeasurementQuantities									 = 19
    id_WLANMeasurementQuantities_Item								 = 20
    id_WLANMeasurementResult										 = 21
    id_TDD_Config_EUTRA_Item										 = 22
    id_Assistance_Information										 = 23
    id_Broadcast													 = 24
    id_AssistanceInformationFailureList								 = 25
    id_SRSConfiguration												 = 26
    id_MeasurementResult											 = 27
    id_TRP_ID														 = 28
    id_TRPInformationTypeListTRPReq									 = 29
    id_TRPInformationListTRPResp									 = 30
    id_MeasurementBeamInfoRequest									 = 31
    id_ResultSS_RSRP												 = 32
    id_ResultSS_RSRQ												 = 33
    id_ResultCSI_RSRP												 = 34
    id_ResultCSI_RSRQ												 = 35
    id_AngleOfArrivalNR												 = 36
    id_GeographicalCoordinates										 = 37
    id_PositioningBroadcastCells									 = 38
    id_LMF_Measurement_ID											 = 39
    id_RAN_Measurement_ID											 = 40
    id_TRP_MeasurementRequestList									 = 41
    id_TRP_MeasurementResponseList									 = 42
    id_TRP_MeasurementReportList									 = 43
    id_SRSType														 = 44
    id_ActivationTime												 = 45
    id_SRSResourceSetID												 = 46
    id_TRPList														 = 47
    id_SRSSpatialRelation											 = 48
    id_SystemFrameNumber											 = 49
    id_SlotNumber													 = 50
    id_SRSResourceTrigger											 = 51
    id_TRPMeasurementQuantities										 = 52
    id_AbortTransmission											 = 53
    id_SFNInitialisationTime										 = 54
    id_ResultNR														 = 55
    id_ResultEUTRA													 = 56
    id_TRPInformationTypeItem										 = 57
    id_CGI_NR														 = 58
    id_SFNInitialisationTime_NR										 = 59
    id_Cell_ID														 = 60
    id_SrsFrequency													 = 61
    id_TRPType														 = 62
    id_SRSSpatialRelationPerSRSResource								 = 63
    id_MeasurementPeriodicityExtended								 = 64
    id_PRS_Resource_ID												 = 65
    id_PRSTRPList													 = 66
    id_PRSTransmissionTRPList										 = 67
    id_OnDemandPRS													 = 68
    id_AoA_SearchWindow												 = 69
    id_TRP_MeasurementUpdateList									 = 70
    id_ZoA															 = 71
    id_ResponseTime													 = 72
    id_UEReportingInformation										 = 73
    id_MultipleULAoA												 = 74
    id_UL_SRS_RSRPP													 = 75
    id_SRSResourcetype												 = 76
    id_ExtendedAdditionalPathList									 = 77
    id_ARPLocationInfo												 = 78
    id_ARP_ID														 = 79
    id_LoS_NLoSInformation											 = 80
    id_UETxTEGAssociationList										 = 81
    id_NumberOfTRPRxTEG												 = 82
    id_NumberOfTRPRxTxTEG											 = 83
    id_TRPTxTEGAssociation											 = 84
    id_TRPTEGInformation											 = 85
    id_TRP_Rx_TEGInformation										 = 86
    id_TRP_PRS_Information_List										 = 87
    id_PRS_Measurements_Info_List									 = 88
    id_PRSConfigRequestType											 = 89
    id_UE_TEG_Info_Request											 = 90
    id_MeasurementTimeOccasion										 = 91
    id_MeasurementCharacteristicsRequestIndicator					 = 92
    id_TRPBeamAntennaInformation									 = 93
    id_NR_TADV														 = 94
    id_MeasurementAmount											 = 95
    id_pathPower													 = 96
    id_PreconfigurationResult										 = 97
    id_RequestType													 = 98
    id_UE_TEG_ReportingPeriodicity									 = 99
    id_SRSPortIndex													 = 100
    id_procedure_code_101_not_to_be_used							 = 101
    id_procedure_code_102_not_to_be_used							 = 102
    id_procedure_code_103_not_to_be_used							 = 103
    id_UETxTimingErrorMargin										 = 104
    id_MeasurementPeriodicityNR_AoA									 = 105
    id_SRSTransmissionStatus										 = 106
    id_nrofSymbolsExtended											 = 107
    id_repetitionFactorExtended										 = 108
    id_StartRBHopping												 = 109
    id_StartRBIndex													 = 110
    id_transmissionCombn8											 = 111


### MEASUREMENT INFORMATION TRANSMISSION

## MeasurementRequest
def MeasurementRequest(nrppatransactionID,id_LMF_Measurement_ID,trpID,reportCharacteristics,tRPMeasurementQuantities ,timingReportingGranularityFactor,optional_fields):
    TRPID=[]
    for id in trpID:
        TRPID.append({'tRP-ID': id})
    
    nrppa_message = ('initiatingMessage', {
        'procedureCode': ProcedureCodeEP.id_Measurement.value,
        'criticality': 'reject',
        'nrppatransactionID': nrppatransactionID,
        'value': ('MeasurementRequest', {'protocolIEs' : [{'id': IEs_id.id_LMF_Measurement_ID.value ,           'criticality': 'reject', 'value': ('Measurement-ID', id_LMF_Measurement_ID)},
                                                          {'id': IEs_id.id_TRP_MeasurementRequestList.value ,   'criticality': 'reject', 'value': ('TRP-MeasurementRequestList',TRPID )},
                                                          {'id': IEs_id.id_ReportCharacteristics.value ,        'criticality': 'reject', 'value': ('ReportCharacteristics',reportCharacteristics )},
                                                          {'id': IEs_id.id_TRPMeasurementQuantities.value ,     'criticality': 'reject', 'value': ('TRPMeasurementQuantities', [ { 'tRPMeasurementQuantities-Item': tRPMeasurementQuantities}] )}
                                                        ]})})
    
    for i in optional_fields:
        new_val = {'id': i[0] , 'criticality': 'ignore', 'value': (i[1],i[2])}
        nrppa_message[1]['value'][1]['protocolIEs'].append(new_val)
    
    return nrppa_message



## MeasurementUpdate
def MeasurementUpdate(nrppatransactionID,id_LMF_Measurement_ID,id_RAN_Measurement_ID, srsConfiguration):
    
    nrppa_message = ('initiatingMessage', {
        'procedureCode': ProcedureCodeEP.id_MeasurementUpdate.value,
        'criticality': 'reject',
        'nrppatransactionID': nrppatransactionID,
        'value': ('MeasurementUpdate', {'protocolIEs' : [{'id': IEs_id.id_LMF_Measurement_ID.value, 'criticality': 'ignore', 'value': ('Measurement-ID', id_LMF_Measurement_ID)},
                                                         {'id': IEs_id.id_RAN_Measurement_ID.value, 'criticality': 'ignore', 'value': ('TRP-MeasurementRequestList', id_RAN_Measurement_ID )},
                                                         {'id': IEs_id.id_SRSConfiguration.value,   'criticality': 'ignore', 'value': ('SRSConfiguration',srsConfiguration)}
                                                                ]})})
    
    return nrppa_message



# MeasurementAbort
def MeasurementAbort(nrppatransactionID,id_LMF_Measurement_ID,id_RAN_Measurement_ID):
    nrppa_message = ('initiatingMessage', {
        'procedureCode': ProcedureCodeEP.id_MeasurementAbort.value,
        'criticality': 'reject',
        'nrppatransactionID': nrppatransactionID,
        'value': ('MeasurementAbort', {'protocolIEs' : [{'id': IEs_id.id_LMF_Measurement_ID.value , 'criticality': 'ignore', 'value': ('Measurement-ID', id_LMF_Measurement_ID )},
                                                        {'id': IEs_id.id_RAN_Measurement_ID.value , 'criticality': 'ignore', 'value': ('Measurement-ID', id_RAN_Measurement_ID)}
                                                                    ]})})
    return nrppa_message



### E- CIDMeasurement 

# E-CIDMeasurementInitiationRequest

def E_CIDMeasurementInitiationRequest(nrppatransactionID,id_UE_Measurement,reportCharacteristics,meas):

    nrppa_message = ('initiatingMessage', {
        'procedureCode': ProcedureCodeEP.id_e_CIDMeasurementInitiation.value,
        'criticality': 'reject',
        'nrppatransactionID': nrppatransactionID, 
        'value': ('E-CIDMeasurementInitiationRequest', {'protocolIEs': [{'id': IEs_id.id_LMF_UE_Measurement_ID.value, 'criticality': 'reject', 'value': ('UE-Measurement-ID',id_UE_Measurement )},
                                                                        {'id': IEs_id.id_ReportCharacteristics.value, 'criticality': 'reject', 'value': ('ReportCharacteristics',reportCharacteristics )}, 
                                                                        {'id': IEs_id.id_MeasurementQuantities.value, 'criticality': 'reject', 'value': ('MeasurementQuantities',[{'id': 11, 'criticality': 'reject', 'value': ('MeasurementQuantities-Item', {'measurementQuantitiesValue':meas  })}  ] )},
                                                                ]})})
    return nrppa_message


# E-CIDMeasurementTerminationCommand
def E_CIDMeasurementTerminationCommand(nrppatransactionID, id_LMF_UE_Measurement_ID, id_RAN_UE_Measurement_ID):
    nrppa_message = ('initiatingMessage', {
        'procedureCode': ProcedureCodeEP.id_e_CIDMeasurementTermination.value,
        'criticality': 'reject',
        'nrppatransactionID': nrppatransactionID,
        'value': ('E-CIDMeasurementTerminationCommand', {'protocolIEs' : [{'id': IEs_id.id_LMF_UE_Measurement_ID.value , 'criticality': 'ignore', 'value': ('UE-Measurement-ID', id_LMF_UE_Measurement_ID )},
                                                                          {'id': IEs_id.id_RAN_UE_Measurement_ID.value , 'criticality': 'ignore', 'value': ('UE-Measurement-ID', id_RAN_UE_Measurement_ID)}
                                                                    ]})})
    return nrppa_message


## OTDOAInformationRequest
def OTDOAInformationRequest(nrppatransactionID, val):
    
    value = list()
    for i in val:
        value.append({'id': 10, 'criticality': 'reject', 'value': ('OTDOA-Information-Type-Item', {'oTDOA-Information-Item': i})}  )

    nrppa_message = ('initiatingMessage', {
            'procedureCode': ProcedureCodeEP.id_oTDOAInformationExchange.value, 
            'criticality': 'reject',
            'nrppatransactionID': nrppatransactionID, 
            'value': ('OTDOAInformationRequest', {'protocolIEs': [{'id': IEs_id.id_OTDOA_Information_Type_Group.value, 'criticality': 'reject', 'value': ('OTDOA-Information-Type', value )}
                                                                    ]})})

    return nrppa_message


## AssistanceInformationControl
def AssistanceInformationControl(nrppatransactionID,systeminfo={},broadcast='start',plmn_id=[b'001'],nr_rancell_id=[(11,36)]):

    systeminfo= {'systemInformation': [{ 'broadcastPeriodicity': 'ms80', 'posSIBs': [{'posSIB-Type': 'posSibType1-1', 'posSIB-Segments': [{'assistanceDataSIBelement': b'1' }]}] }]  }


    val=[]
    for i,j in plmn_id,nr_rancell_id:
        val.append({'pLMN-Identity': i, 'nG-RANcell':  ('nR-CellID',j )})
    nrppa_message = ('initiatingMessage', {
            'procedureCode': ProcedureCodeEP.id_assistanceInformationControl.value, 
            'criticality': 'reject',
            'nrppatransactionID': nrppatransactionID, 
            'value': ('AssistanceInformationControl', {'protocolIEs' : [{'id': IEs_id.id_Assistance_Information.value , 'criticality': 'ignore', 'value': ('Assistance-Information', systeminfo )},
                                                                        {'id': IEs_id.id_Broadcast.value , 'criticality': 'ignore', 'value': ('Broadcast', broadcast)},
                                                                        {'id': IEs_id.id_PositioningBroadcastCells.value , 'criticality': 'ignore', 'value': ('PositioningBroadcastCells',   val )}
                                                                        ]})})
    return nrppa_message




## ErrorIndication
def ErrorIndication(nrppatransactionID,error):
    nrppa_message = ('initiatingMessage', {
        'procedureCode': ProcedureCodeEP.id_errorIndication.value,
        'criticality': 'ignore',
        'nrppatransactionID': nrppatransactionID,
        'value': ('ErrorIndication', {'protocolIEs' : [{'id': IEs_id.id_Cause.value, 'criticality': 'ignore', 'value': ('Cause', error)}]})})
    
    return nrppa_message



## PositioningInformationRequest 
def PositioningInformationRequest(nrppatransactionID,RequestedSRSTx, UEReportingInfo, UE_TEG_Info_Request):
    nrppa_message = ('initiatingMessage', {
        'procedureCode': ProcedureCodeEP.id_positioningInformationExchange.value,
        'criticality': 'reject',
        'nrppatransactionID': nrppatransactionID,
        'value': ('PositioningInformationRequest', {'protocolIEs' : [{'id': IEs_id.id_RequestedSRSTransmissionCharacteristics.value , 'criticality': 'ignore', 'value': ('RequestedSRSTransmissionCharacteristics',RequestedSRSTx )},
                                                                    {'id': IEs_id.id_UEReportingInformation.value , 'criticality': 'ignore', 'value': ('UEReportingInformation',UEReportingInfo )},
                                                                    {'id': IEs_id.id_UE_TEG_Info_Request.value , 'criticality': 'ignore', 'value': ('UE-TEG-Info-Request', UE_TEG_Info_Request )}
                                                                    ]})})
    return nrppa_message



##  PositioningActivationRequest 
def PositioningActivationRequest(nrppatransactionID,SRSType):
    nrppa_message = ('initiatingMessage', {
        'procedureCode': ProcedureCodeEP.id_positioningActivation.value,
        'criticality': 'reject',
        'nrppatransactionID': nrppatransactionID,
        'value': ('PositioningActivationRequest', {'protocolIEs' : [{'id': IEs_id.id_SRSType.value , 'criticality': 'ignore', 'value': ('SRSType', SRSType )}
                                                                    ]})})
    return nrppa_message



## PositioningDeactivation
def PositioningDeactivation(nrppatransactionID,value):
    nrppa_message = ('initiatingMessage', {
        'procedureCode': ProcedureCodeEP.id_positioningDeactivation.value,
        'criticality': 'ignore',
        'nrppatransactionID': nrppatransactionID,
        'value': ('PositioningDeactivation', {'protocolIEs' : [{'id': IEs_id.id_AbortTransmission.value , 'criticality': 'ignore', 'value': ('AbortTransmission', value )},
                                                                    ]})})
    return nrppa_message


#### TRP INFORMATION TX
def TRPInformationRequest(nrppatransactionID,val):
    value=[]
    for i in val:
        value.append( {'id': 57, 'criticality': 'reject', 'value': ('TRPInformationTypeItem', i )})

    nrppa_message = ('initiatingMessage', {
            'procedureCode': ProcedureCodeEP.id_tRPInformationExchange.value, 
            'criticality': 'reject',
            'nrppatransactionID': nrppatransactionID, 
            'value': ('TRPInformationRequest', {'protocolIEs' : [ {'id': IEs_id.id_TRPList.value , 'criticality': 'ignore', 'value': ('TRPList',[{'tRP-ID':1}]  )},
                                                                  {'id': IEs_id.id_TRPInformationTypeListTRPReq.value , 'criticality': 'reject', 'value': ('TRPInformationTypeListTRPReq', value )}
                                                                        ]})})
    
    return nrppa_message



## PRSConfigurationRequest
def PRSConfigurationRequest(nrppatransactionID,prsConfigRequestType,trp_id):
    nrppa_message = ('initiatingMessage', {
            'procedureCode': ProcedureCodeEP.id_pRSConfigurationExchange.value, 
            'criticality': 'reject',
            'nrppatransactionID': nrppatransactionID, 
            'value': ('PRSConfigurationRequest', {'protocolIEs' : [ {'id': IEs_id.id_PRSConfigRequestType.value , 'criticality': 'ignore', 'value': ('PRSConfigRequestType',prsConfigRequestType)},
                                                                    {'id': IEs_id.id_PRSTRPList.value , 'criticality': 'ignore', 'value': ('PRSTRPList', [{ 'tRP-ID': trp_id,'requestedDLPRSTransmissionCharacteristics': { 'requestedDLPRSResourceSet-List': [{'pRSbandwidth':10, 'combSize': 'n4' }]  }}])} ]}            
                                                )})
                                                                        
    return nrppa_message





## MeasurementPreconfigurationRequired
# TODO -> pass to the function the values of the parameters of the NRPPa message
def MeasurementPreconfigurationRequired(nrppatransactionID):
    prsresource= [ {'pRSResourceID': 4, 'sequenceID':12, 'rEOffset':1, 'resourceSlotOffset':32, 'resourceSymbolOffset':1}]
    prsset1={'pRSResourceSetID':5 ,'subcarrierSpacing': 'kHz30', 'pRSbandwidth': 10, 'startPRB':11, 'pointA':1, 'combSize': 'n4', 'cPType': 'normal', 'resourceSetPeriodicity': 'n4', 'resourceSetSlotOffset': 9, 'resourceRepetitionFactor':'rf1', 'resourceTimeGap': 'tg1', 'resourceNumberofSymbols': 'n12', 'pRSResourceTransmitPower': 20, 'pRSResource-List':  prsresource}
    prsConfigRequestType= [ {'tRP-ID': 10 , 'nR-PCI': 13 , 'pRSConfiguration': {'pRSResourceSet-List': [prsset1]} }]
    
    nrppa_message = ('initiatingMessage', {
            'procedureCode': ProcedureCodeEP.id_measurementPreconfiguration.value, 
            'criticality': 'reject',
            'nrppatransactionID': nrppatransactionID, 
            'value': ('MeasurementPreconfigurationRequired', {'protocolIEs' : [ {'id': IEs_id.id_TRP_PRS_Information_List.value , 'criticality': 'ignore', 'value': ('TRP-PRS-Information-List',prsConfigRequestType)}]}
                                                                                    )})                       
    return nrppa_message



##MeasurementActivation
# TODO -> pass to the function the values of the parameters of the NRPPa message
def MeasurementActivation(nrppatransactionID,requesttype):
    nrppa_message = ('initiatingMessage', {
            'procedureCode': ProcedureCodeEP.id_measurementActivation.value, 
            'criticality': 'reject',
            'nrppatransactionID': nrppatransactionID, 
            'value': ('MeasurementActivation', {'protocolIEs' : [ {'id': IEs_id.id_RequestType.value , 'criticality': 'ignore', 'value': ('RequestType',requesttype)},
                                                                  {'id': IEs_id.id_PRS_Measurements_Info_List.value , 'criticality': 'ignore', 'value': ('PRS-Measurements-Info-List',[{'pointA': 11, 'measPRSPeriodicity':'ms20','measPRSOffset':22,'measurementPRSLength': 'ms3'}] )}]}
                                                                                    )})
    return nrppa_message                                                                        


