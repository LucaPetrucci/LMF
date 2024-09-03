#!/bin/bash
envoy -c /etc/envoy/envoy.yaml >/etc/envoy/envoy.log 2>&1 &
python src/lmf_server_api.py
# sleep 99999