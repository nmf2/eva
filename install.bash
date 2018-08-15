#!/bin/bash

checkInstall(){
    checkcmd=$($1)
    expr=$2
    install=$3
    # check if the expression is in the output of the check command 
    if [[ "$checkcmd" != *"$expr"* ]]; then
        echo "Package not present. Installing (sudo is needed):"
        $(install)
    else
        echo "Package installed"
    fi
}
echo "Checking Pip3 installation"
checkInstall "pip3 -V" "python3" "sudo apt-get install python3-pip"

pip3 install -r requirements.txt

echo "Need sudo to install eva's package: "
sudo python3 setup.py install
