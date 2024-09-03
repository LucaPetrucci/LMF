#!/bin/bash


curl -X POST http://lmf_net.org:4321/nlmf-loc/v1/cancel-location -H 'Content-Type: application/json' -d '{ "hgmlcCallBackURI": "", "ldrReference": "01" }'
