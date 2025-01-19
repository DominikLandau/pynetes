#!/bin/bash

if command -v helm 2>&1 >/dev/null
then
    curl -LO https://get.helm.sh/helm-v3.17.0-rc.1-linux-arm64.tar.gz
    tar -zxvf helm-v3.17.0-rc.1-linux-arm64.tar.gz
    sudo install -m 755 linux-amd64/helm /usr/local/sbin/helm
fi

helm repo add csi-driver-nfs https://raw.githubusercontent.com/kubernetes-csi/csi-driver-nfs/master/charts
helm install csi-driver-nfs csi-driver-nfs/csi-driver-nfs --namespace nfs --version v4.9.0 --create-namespace