#!/bin/bash

# Curl request with name instead of IP
curl -X POST http://lmf_net.org:4321/nlmf-loc/v1/determine-location -H 'Content-Type: application/json' -d '{"externalClientType":"PLMN_OPERATOR_SERVICES","correlationID":"lcs type 0","locationQoS":{"hAccuracy":3,"verticalRequested":false,"responseTime":"DELAY_TOLERANT","lcsQosClass":"BEST_EFFORT"},"supi":"001010000000001"}'
#curl -X POST http://lmf_net.org:4321/nlmf-loc/v1/determine-location -H 'Content-Type: application/json' -d '{"externalClientType":"PLMN_OPERATOR_SERVICES","correlationID":"lcs type 0","locationQoS":{"hAccuracy":3,"verticalRequested":false,"responseTime":"NO_DELAY","lcsQosClass":"BEST_EFFORT"},"supi":"001010000000001"}'
#curl -X POST http://lmf_net.org:4321/nlmf-loc/v1/determine-location -H 'Content-Type: application/json' -d '{"externalClientType":"PLMN_OPERATOR_SERVICES","correlationID":"lcs type 0","locationQoS":{"hAccuracy":3,"verticalRequested":false,"responseTime":"LOW_DELAY","lcsQosClass":"MULTIPLE_QOS"},"supi":"001010000000001"}'

# curl -X POST http://lmf_net.org:4321/nlmf-loc/v1/determine-location -H 'Content-Type: application/json' -d '{"ldrType": "UE_AVAILABLE", "hgmlcCallBackURI": "", "ldrReference": "01" , "maxRespTime": 60, "externalClientType":"PLMN_OPERATOR_SERVICES","correlationID":"lcs type 0","locationQoS":{"hAccuracy":3,"verticalRequested":false,"responseTime":"DELAY_TOLERANT","lcsQosClass":"BEST_EFFORT"},"supi":"001010000000001"}'
