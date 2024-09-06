# 3GPP Location Management Function (LMF) Release 17


Welcome to the LMF (Location Management Function) Network Function implementation repository.
 This repository contains the source code and instructions for deploying and using the LMF in a core network environment.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [License](#license)


## Cite Us
The description of the compliant 3GPP LMF and the implementation status of 5G position entities have been accepted and will be published in IEEE 100th Vehicular Technology Conference (VTC2024-Fall). 

If you use this tool in your research or project, please cite the following paper:
 
 ```
S. Zanini, L. Petrucci, I. Palamà, G. Bianchi, and S. Bartoletti, “Towards End-to-end Implementation of 5G Positioning with Off-the-shelf Devices,” 2024 IEEE 100th Vehicular Technology Conference (VTC2024-Fall)
 ```


## Overview

The Location Management Function (LMF) is a crucial component in modern telecommunication networks, responsible for managing and providing location services. This implementation adheres to the latest standards and can be seamlessly integrated into existing core network setups.

## Features

- Standard-compliant LMF implementation
- Easy integration with existing core network components
- Scalable and configurable architecture
- Possibilities to add localization algorithms

## Installation

### Prerequisites
Containerized 5G Core Network up and running, we have tested the LMF with the [Free5GC](https://free5gc.org/) and [OAI-5G Core Network](https://openairinterface.org/oai-5g-core-network-project/).
For the Free5GC core we use a patched version of the `AMF`, the image is available 
```bash
docker pull lucapetrucci/free5gc-amf
```
The following steps outline how to run the LMF

### 1. Clone the repository
```bash
git clone https://github.com/LucaPetrucci/LMF.git
# enter in the directory
cd LMF
docker build -f Dockerfile -t lmf:latest
```
### 2. Build the Docker Image
```
docker build -f Dockerfile -t lmf:latest
```
### 3. Run the LMF
There are two available methods for running the LMF within the 5G core. Whatever method is chosen, the configuration file `LMF/src/config.py` must be updated according to your network setup. This file will be mounted as volume to the LMF Docker Dontainer and used by the LMF Python Script.



```bash
cd LMF/src
nano config.py
```

#### Method 1: Run the LMF as a Docker Container inside the same network of the 5G Core

You can execute the LMF as a Docker container within the 5G core by following the procedure outlined below. This method allows for easier deployment and isolation within the core environment.


```bash
docker compose -f docker-compose-lmf.yaml up
```
After start-up the LMF is up and running and it will be possible to see the LMF log.

#### Method 2: Run the LMF as a Python Script on the Host Machine
Alternatively, you can start the LMF as a Python script directly on the host machine that runs the dockerized 5G core.
This solution is preferable during development and debugging of the component, but requires some extra configuration.
- Properly configure the routing between LMF and 5G Core

- Configure and start the proxy envoy on the host machine to forward requests from the core to the LMF

Edit the `envoy.yaml`in the `LMF/envoy_proxy` folder to match the LMF IP address.
```bash
cd LMF/envoy_proxy

# update the endpoints section of the file with the LMF address
    
    endpoints:
    - lb_endpoints:
    - endpoint:
        address:
            socket_address:
            address: LMF_ADDRESS # LMF Address
            port_value: 4321 # LMF Port

# Run the envoy proxy
envoy -c envoy.yaml
```


**Install Requirements:**

Ensure you have Python and pip installed. Then, run:
```bash
# Run the pip command inside the 'src' folder of the repository
cd LMF/src
pip install -r requirements.txt
```

**Run LMF:**
```bash
# Run the LMF python script
cd LMF
python src/lmf_server_api.py
```

## Acknowledge
This software is supported by:
- 6G-SANDBOX, Horizon Europe funded research project
- FIND-OUT project founded by an European Research Council grant
- Italian PNRR RESTART Program

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
