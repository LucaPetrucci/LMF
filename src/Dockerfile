from ubuntu:jammy



# Install python
# ENV TZ=Europe/Rome
RUN apt update
RUN apt upgrade -y
RUN apt install curl software-properties-common apt-transport-https gnupg2 lsb-release vim -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive TZ=Europe/Rome apt install python3.12 -y
RUN apt install python-is-python3
RUN ln -sf /usr/bin/python3.12 /usr/bin/python3

# Install pip
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12


# Install envoy
RUN apt update
RUN curl -sL 'https://deb.dl.getenvoy.io/public/gpg.8115BA8E629CC074.key' | gpg --dearmor -o /usr/share/keyrings/getenvoy-keyring.gpg
RUN echo a077cb587a1b622e03aa4bf2f3689de14658a9497a9af2c427bba5f4cc3c4723 /usr/share/keyrings/getenvoy-keyring.gpg | sha256sum --check
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/getenvoy-keyring.gpg] https://deb.dl.getenvoy.io/public/deb/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/getenvoy.list
RUN apt update
RUN apt install -y getenvoy-envoy


COPY src/requirements.txt LMF/src/

RUN pip install --ignore-installed -r LMF/src/requirements.txt
RUN pip install --force-reinstall websocket-client


COPY ../envoy_proxy/envoy.yaml /etc/envoy/envoy.yaml

COPY pytdoa/ LMF/pytdoa/
COPY LICENSE LMF/
# COPY src/config.py LMF/src/
COPY src/HandleLocation.py src/lmf_instance.py src/lmf_server_api.py src/LPP_handler.py src/LPP_message_gen.py LMF/src/
COPY src/custom_log.py src/NRPPa_handler.py src/NRPPa_message_gen.py src/positiong_algorithm.py src/requirements.txt LMF/src/
COPY src/start.sh LMF/


# RUN envoy -c /etc/envoy/envoy.yaml &

WORKDIR LMF

CMD [ "/bin/bash", "start.sh"]