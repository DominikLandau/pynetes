#!/bin/bash

if command -v kubelet 2>&1 >/dev/null
then
    echo "kubelet exists"
    exit 0
fi

### kubectl, kubeadm, kubelet
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt-get update

sudo apt install -y kubectl=1.31* kubeadm=1.31* kubelet=1.31* 
sudo apt-mark hold kubelet kubeadm kubectl
sudo systemctl enable --now kubelet