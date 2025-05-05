#install script for Maltime dependencies

#!/bin/bash

echo "Installing dependencies for Maltime..."

#make sure script is run as root
if ["$EUID" -ne 0]; then
	echo "Please run as root"
	exit
fi

#update packages and install dependencies
echo "updating system packages and installing MalTime dependencies"

apt update

apt install -y python3 python3-pip

pip3 install flask

echo "Installation Successful!"
echo " "
echo "Usage: python3 app.py --logpath /path/to/cuckoo/log/file.log"
