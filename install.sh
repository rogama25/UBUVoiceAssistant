#!/bin/bash

USERNAME=$SUDO_USER
GREEN='\033[0;32m'
NC='\033[0m'
DIR=`pwd`

set -e

help() {
  echo "UBUVoiceAssistant installer"
  echo "Available options:"
  echo "\"install.sh install\" to install the program"
  echo "\"install.sh install --manual\" to install without autocompleting Mycroft prompts"
  echo "\"install.sh uninstall\" to remove the program"
  echo "\"install.sh update-skills\" to update all the ubu-skills"
  echo "\"install.sh update\" to update UBUVoiceAssistant and ubu-skills"
} 

install() {
  # Refresh system packages
  printf "${GREEN}Updating system packages...${NC}\n"
  apt-get update
  printf "${GREEN}Finished updating system packages${NC}\n"

  # Get python packages
  printf "${GREEN}Installing system dependencies...${NC}\n"
  apt-get install python3-pip python3-pyqt5 python3-pyqt5.qtwebengine git -y
  pip3 install mycroft-messagebus-client babel bs4
  sudo apt install libjack-dev libjack0 -y
  printf "${GREEN}Finished installing system dependencies${NC}\n"

  # Prepare user folder
  sudo -u $USERNAME mkdir -p /home/${USERNAME}/.config/UBUVoiceAssistant
  sudo -u $USERNAME mkdir -p /home/${USERNAME}/.mycroft

  printf "${GREEN}Downloading Mycroft...${NC}\n"
  mkdir -p /usr/lib/mycroft-core
  chown $USERNAME /usr/lib/mycroft-core
  cd /usr/lib/mycroft-core
  sudo -u $USERNAME git clone https://github.com/MycroftAI/mycroft-core.git .
  printf "${GREEN}Finished downloading Mycroft${NC}\n"

  printf "${GREEN}Configuring Mycroft...${NC}\n"
  if [[ -n $1 && $1 == "--manual" ]]; then
    printf "${GREEN}A list of questions will be asked now to configure Mycroft. Answer by pressing Y in all of them.\n"
    printf "Se van a hacer una serie de preguntas para configurar Mycroft. Responde a todas pulsando Y${NC}\n"
    read -s -p "Press Enter to continue."
    sudo -u $USERNAME bash dev_setup.sh -sm
  else
    echo -e YYYYYYYYYYY | sudo -u $USERNAME bash dev_setup.sh -sm
  fi
  printf "${GREEN}Finished configuring Mycroft${NC}\n"

  # Copy UBU skills inside
  printf "${GREEN}Installing UBU skills...${NC}\n"
  cd $DIR
  sudo -u $USERNAME /usr/lib/mycroft-core/bin/mycroft-msm install https://github.com/ubu-skills/ubu-messages
  sudo -u $USERNAME /usr/lib/mycroft-core/bin/mycroft-msm install https://github.com/ubu-skills/ubu-grades
  sudo -u $USERNAME /usr/lib/mycroft-core/bin/mycroft-msm install https://github.com/ubu-skills/ubu-course
  sudo -u $USERNAME /usr/lib/mycroft-core/bin/mycroft-msm install https://github.com/ubu-skills/ubu-help
  sudo -u $USERNAME /usr/lib/mycroft-core/bin/mycroft-msm install https://github.com/ubu-skills/ubu-calendar
  printf "${GREEN}Installed UBU skills${NC}\n"

  # Installing to a permanent location
  printf "${GREEN}Installing to a permanent location...${NC}\n"
  mkdir -p /usr/lib/UBUVoiceAssistant
  echo "#!/bin/bash" > /usr/bin/UBUVoiceAssistant
  echo "cd /usr/lib/UBUVoiceAssistant" >> /usr/bin/UBUVoiceAssistant
  echo "python3 -m UBUVoiceAssistant.GUI.main" >> /usr/bin/UBUVoiceAssistant
  chmod a+x /usr/bin/UBUVoiceAssistant
  cp -r ./src/UBUVoiceAssistant/ /usr/lib/UBUVoiceAssistant
  printf "${GREEN}Installed to a permanent location${NC}\n"

  # Create app launcher icon
  printf "${GREEN}Creating app launcher icon...${NC}\n"
  echo "[Desktop Entry]" > /usr/share/applications/UBUVoiceAssistant.desktop
  echo "Type=Application" >> /usr/share/applications/UBUVoiceAssistant.desktop
  echo "Name=UBUVoiceAssistant" >> /usr/share/applications/UBUVoiceAssistant.desktop
  echo "Comment=UBUVoiceAssistant" >> /usr/share/applications/UBUVoiceAssistant.desktop
  echo "Terminal=false" >> /usr/share/applications/UBUVoiceAssistant.desktop
  echo "Exec=UBUVoiceAssistant" >> /usr/share/applications/UBUVoiceAssistant.desktop
  echo "Icon=/usr/lib/UBUVoiceAssistant/UBUVoiceAssistant/imgs/appicon.png" >> /usr/share/applications/UBUVoiceAssistant.desktop
  echo "Categories=Utility;Education;Accessibility;Qt;" >> /usr/share/applications/UBUVoiceAssistant.desktop
  xdg-desktop-menu forceupdate
  printf "${GREEN}Created app launcher icon${NC}\n"
  printf "${GREEN}Install completed :)${NC}\n"
}

uninstall() {
  rm -rf /usr/lib/UBUVoiceAssistant
  rm -rf /usr/lib/mycroft-core
  rm -f /usr/bin/UBUVoiceAssistant
  rm -f /usr/share/applications/UBUVoiceAssistant.desktop
  rm -rf /home/${USERNAME}/.mycroft
  rm -rf /opt/mycroft
  printf "${GREEN}UBUVoiceAssistant was uninstalled.${NC}\n"
}

updateskills() {
  sudo -u $USERNAME /usr/lib/mycroft-core/bin/mycroft-msm update
}

updateall() {
  rm -rf /usr/lib/UBUVoiceAssistant
  mkdir -p /usr/lib/UBUVoiceAssistant
  cp -r ./src/UBUVoiceAssistant/ /usr/lib/UBUVoiceAssistant
  updateskills
}

if [[ -n $1 && $1 == "install" || $1 == "uninstall" || $1 == "update-skills" || $1 == "update" ]]; then
  # Checking if the script was launched as root
  if [ "$EUID" -ne 0 ]
    then echo "Please, run again the script as sudo."
    exit
  fi
  if [ $1 == "install" ]; then
    install $2
  elif [ $1 == "update-skills" ]; then
    updateskills
  elif [ $1 == "update" ]; then
    updateall
  else
    uninstall
  fi
else
  help
fi
