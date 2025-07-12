FROM ubuntu:jammy

# Install dependencies, Python 3.12, and pip in one layer
RUN apt update && \
    apt upgrade -y && \
    apt install -y curl software-properties-common apt-transport-https gnupg2 lsb-release vim ca-certificates && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt update && \
    DEBIAN_FRONTEND=noninteractive TZ=Europe/Rome apt install -y python3.12 python-is-python3 && \
    ln -sf /usr/bin/python3.12 /usr/bin/python3 && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12 && \
    rm -rf /var/lib/apt/lists/*

# Install Envoy
RUN curl -sL 'https://apt.envoyproxy.io/signing.key' | gpg --dearmor -o /usr/share/keyrings/envoy-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/envoy-keyring.gpg] https://apt.envoyproxy.io $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/envoy.list && \
    apt update && \
    apt install -y envoy && \
    rm -rf /var/lib/apt/lists/*

# Copy source files and install Python dependencies
COPY src/requirements.txt LMF/src/
RUN pip install --ignore-installed -r LMF/src/requirements.txt && \
    pip install --force-reinstall websocket-client

COPY ../envoy_proxy/envoy.yaml /etc/envoy/envoy.yaml
COPY LICENSE LMF/
COPY src/*.py LMF/src/
COPY src/start.sh LMF/

WORKDIR LMF

CMD [ "/bin/bash", "start.sh" ]