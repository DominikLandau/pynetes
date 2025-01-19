#!/bin/bash

if [ "$(kubectl get nodes master -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}')" == "True" ]
then
    echo "cluster exists"
    exit 0
fi

sudo kubeadm init --pod-network-cidr=10.200.0.0/16 --ignore-preflight-errors=all

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# https://docs.tigera.io/calico/latest/getting-started/kubernetes/quickstart
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.29.1/manifests/tigera-operator.yaml
curl -LO https://raw.githubusercontent.com/projectcalico/calico/v3.29.1/manifests/custom-resources.yaml
sed -i 's/cidr: 192.168.0.0\/16/cidr: 10.200.0.0\/16/' custom-resources.yaml
kubectl apply -f custom-resources.yaml

while [ "$(kubectl get nodes -o 'jsonpath={..status.conditions[?(@.type=="Ready")].status}')" != "True" ]; do
    echo "Waiting for Control Plane to become Ready ..."
    sleep 10
done

