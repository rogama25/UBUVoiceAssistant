#!/bin/bash

# Checking if the script was launched as root
if [ "$EUID" -ne 0 ]
  then echo "Por favor, vuelve a ejecutar el script usando sudo"
  exit
fi

USERNAME=$SUDO_USER

# Refresh system packages
apt-get update

# Get python packages
apt-get install python3-pip python3-pyqt5 -y
pip3 install mycroft-messagebus-client

# Add docker dependencies
apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common -y

# Add Docker repo
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) stable"

# Force-refresh packages
apt-get update

# Install Docker
apt-get install docker-ce docker-ce-cli containerd.io

# Get Mycroft Docker image
docker pull mycroftai/docker-mycroft

# Prepare user folder
sudo -u $USERNAME mkdir -p ~/.config/mycroft-docker

# Create docker container
sudo -u $USERNAME docker create -v ~/.config/mycroft-docker:/root/.mycroft \
    --device /dev/snd -e PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native \
    -v ${XDG_RUNTIME_DIR}/pulse/native:${XDG_RUNTIME_DIR}/pulse/native \
    -v ~/.config/pulse/cookie:/root/.config/pulse/cookie \
    -p 8181:8181 --name mycroft mycroftai/docker-mycroft

# Copy UBU skills inside
sudo -u $USERNAME docker cp ./src/skills/. mycroft:/opt/mycroft/skills