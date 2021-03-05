#!/bin/bash

USERNAME=$SUDO_USER
GREEN='\033[0;32m'
NC='\033[0m'

help() {
  echo "UBUVoiceAssistant installer"
  echo "Available options:"
  echo "\"install.sh install\" to install the program"
  echo "\"install.sh uninstall\" to remove the program"
} 

install() {
  # Refresh system packages
  printf "${GREEN}Updating system packages...${NC}\n"
  apt-get update
  printf "${GREEN}Finished updating system packages${NC}\n"

  # Get python packages
  printf "${GREEN}Installing system dependencies...${NC}\n"
  apt-get install python3-pip python3-pyqt5 -y
  pip3 install mycroft-messagebus-client
  printf "${GREEN}Finished installing system dependencies${NC}\n"

  # Add docker dependencies
  printf "${GREEN}Downloading docker dependencies...${NC}\n"
  apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common -y
  printf "${GREEN}Finished downloading docker dependencies${NC}\n"

  # Add Docker repo
  printf "${GREEN}Adding docker repository for Ubuntu...${NC}\n"
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
  add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable"
  printf "${GREEN}Finished adding docker repository${NC}\n"

  # Force-refresh packages
  printf "${GREEN}Refreshing packages...${NC}\n"
  apt-get update
  printf "${GREEN}Finished refreshing packages${NC}\n"

  # Install Docker
  printf "${GREEN}Installing docker...${NC}\n"
  apt-get install docker-ce docker-ce-cli containerd.io
  printf "${GREEN}Finished installing docker${NC}\n"

  # Get Mycroft Docker image
  printf "${GREEN}Getting Mycroft image from docker...${NC}\n"
  docker pull mycroftai/docker-mycroft
  printf "${GREEN}Mycroft image downloaded${NC}\n"

  # Prepare user folder
  sudo -u $USERNAME mkdir -p /home/${USERNAME}/.config/mycroft-docker

  # Create docker container
  printf "${GREEN}Creating docker container...${NC}\n"
  sudo -u $USERNAME docker create -v /home/${USERNAME}/.config/mycroft-docker:/root/.mycroft \
      --device /dev/snd -e PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native \
      -v ${XDG_RUNTIME_DIR}/pulse/native:${XDG_RUNTIME_DIR}/pulse/native \
      -v ~/.config/pulse/cookie:/root/.config/pulse/cookie \
      -p 8181:8181 --name mycroft mycroftai/docker-mycroft
  printf "${GREEN}Created docker container${NC}\n"

  # Copy UBU skills inside
  printf "${GREEN}Installing UBU skills...${NC}\n"
  sudo -u $USERNAME docker cp ./src/skills/. mycroft:/opt/mycroft/skills
  printf "${GREEN}Installed UBU skills${NC}\n"

  # Installing to a permanent location
  printf "${GREEN}Installing to a permanent location...${NC}\n"
  mkdir -p /usr/lib/UBUVoiceAssistant
  echo "#!/bin/bash" > /usr/bin/UBUVoiceAssistant
  echo "cd /usr/lib/UBUVoiceAssistant" >> /usr/bin/UBUVoiceAssistant
  echo "python3 -m GUI.main" >> /usr/bin/UBUVoiceAssistant
  cp ./src/. /usr/lib/UBUVoiceAssistant
  printf "${GREEN}Installed to a permanent location${NC}\n"

  # Create app launcher icon
  printf "${GREEN}Creating app launcher icon...${NC}\n"
  echo "[Desktop Entry]" > /usr/share/applications/UBUVoiceAssistant.desktop
  echo "Type=Application" >> /usr/share/applications/UBUVoiceAssistant.desktop
  echo "Name=UBUVoiceAssistant" >> /usr/share/applications/UBUVoiceAssistant.desktop
  echo "Comment=UBUVoiceAssistant" >> /usr/share/applications/UBUVoiceAssistant.desktop
  echo "Terminal=false" >> /usr/share/applications/UBUVoiceAssistant.desktop
  echo "Exec=UBUVoiceAssistant" >> /usr/share/applications/UBUVoiceAssistant.desktop
  echo "Icon=UBUVoiceAssistant.png" >> /usr/share/applications/UBUVoiceAssistant.desktop
  echo "Categories=Utility;Education;Accessibility;Qt;" >> /usr/share/applications/UBUVoiceAssistant.desktop
  printf "${GREEN}Created app launcher icon${NC}\n"
}

uninstall() {
  rm -rf /usr/lib/UBUVoiceAssistant
  rm -f /usr/lib/UBUVoiceAssistant
  rm -f /usr/share/applications/UBUVoiceAssistant.desktop
  printf "${GREEN}UBUVoiceAssistant was uninstalled. You may want to remove the docker containers to free space using the following commands:${NC}\n"
  echo "docker rm -v mycroft"
  echo "docker image rm mycroftai/docker-mycroft"
}

if [[ $1 == "install" || $1 == "uninstall" ]]; then
  # Checking if the script was launched as root
  if [ "$EUID" -ne 0 ]
    then echo "Please, run again the script as sudo."
    exit
  fi
  if [ $1 = "install" ]; then
    install
  else
    uninstall
  fi
else
  help
fi