[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=rogama25_UBUVoiceAssistant&metric=alert_status)](https://sonarcloud.io/dashboard?id=rogama25_UBUVoiceAssistant)
# UBUVoiceAssistant
UBUVoiceAssistant es una aplicación de escritorio que utiliza un asistente de voz, Mycroft, para que, mediante comandos de voz o texto, el usuario pueda interactuar con una plataforma Moodle.

**Desarollado por Rodrigo Garcia Martin para el trabajo de fin de grado 2021 de Ingeniería informática en la Universidad de Burgos**

<div>Application icon made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

## Usage
Read this in Spanish [here](https://github.com/rogama25/UBUVoiceAssistant/blob/master/docs/anexos.pdf), from page 29.
### Requirements
* Windows 10 (recommended to have latest version) or Ubuntu (recommended latest LTS or stable)
* 4GB RAM for Ubuntu, 6GB for Windows
* 5GB free on disk

### Install
You need a CPU that supports AVX technology. Check if you have it on Linux: `cat /proc/cpuinfo | grep avx`

If you are using a virtual machine and you have Hyper-V enabled on Windows, Ubuntu won't detect AVX and you will need to disable Hyper-V using these commands in a Powershell as admin:
```
bcdedit /set hypervisorlaunchtype off
DISM /Online /Disable-Feature:Microsoft-Hyper-V
Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-Hypervisor
```

Enable them back after you have finished using the project using these:
```
bcdedit /set hypervisorlaunchtype auto
DISM /Online /Enable-Feature:Microsoft-Hyper-V
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V-Hypervisor
```

#### Windows
You will need to enable WSL. Follow [this guide](https://docs.microsoft.com/en-us/windows/wsl/install-win10#step-1---enable-the-windows-subsystem-for-linux), steps 1 to 5. On step 6, install Ubuntu LTS or latest from the Microsoft Store.

After that, you need to download and start VcXserv from [here](https://sourceforge.net/projects/vcxsrv/). Don't forget to disable access control. Add these lines to ~/.bashrc:

Only if using WSL 1: `export DISPLAY=:0`

Only if using WSL 2: `export DISPLAY=$(awk'/nameserver / {print $2; exit}'/etc/resolv.conf 2>/dev/null):0`

`export LIBGL_ALWAYS_INDIRECT=1`

Download Pulse binaries from [here](https://www.freedesktop.org/wiki/Software/PulseAudio/Ports/Windows/Support/). Edit `etc/pulse/default.pa` and add these lines:
```
load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1
load-module module-waveout sink_name=output source_name=input record=1
```
Add this line to `etc/pulse/daemon.conf`:

`exit-idle-time = -1`

Finally, add this to ~/.bashrc:

If using WSL 1: `export PULSE_SERVER=tcp:127.0.0.1`

If using WSL 2: `export PULSE_SERVER=tcp:$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null)`

Run bin/pulseaudio.exe in a terminal

You will need to do the Ubuntu part too

#### Ubuntu
##### If you can access a browser
Get the source code for the last release and extract it anywhere. cd into the extracted folder and run `sudo ./install.sh install`. After it finishes, you will have an icon in the Ubuntu's app launcher or you can run `UBUVoiceAssistant` in a terminal.

If it gets stuck in an interactive part, run `sudo ./install.sh uninstall` and then `sudo ./install.sh install --manual`

##### If you can't
Run these commands:
```
sudo apt update
sudo apt install git
git clone https://github.com/rogama25/UBUVoiceAssistant.git
cd UBUVoiceAssistant
sudo ./install.sh install
```

After that, launch the program through Ubuntu's app launcher or running `UBUVoiceAssistant`

If it gets stuck in an interactive part, run `sudo ./install.sh uninstall` and then `sudo ./install.sh install --manual`

If you encounter an error when running the project in WSL that says `“ImportError: libQt5Core.so.5: cannot open shared object file: No such file or directory`, [it's a known bug](https://github.com/microsoft/WSL/issues/3023), and you can run this as a workaround:

`sudo strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5`

## Development
It's recommended to follow along the usage instructions because it will install automatically all dependencies. Then you will have the UI at `/usr/lib/UBUVoiceAssistant`, and skills at `/opt/mycroft/skills`. Mycroft will be located at `usr/lib/mycroft-core`

It's recommended that you install QtDesigner using `sudo apt-get install qttools5-dev-tools` and poedit `sudo apt install poedit`. Also recommended to use mypy and pylint, using the files in the `scripts` folder.

Detailed and manual way explained in Spanish [here](https://github.com/rogama25/UBUVoiceAssistant/blob/master/docs/anexos.pdf), from page 21.