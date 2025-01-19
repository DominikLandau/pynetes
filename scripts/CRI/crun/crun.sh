#!/bin/bash

if command -v crun 2>&1 >/dev/null
then
    echo "crun exists"
    exit 0
fi

sudo apt-get install -y make git gcc build-essential pkgconf libtool libsystemd-dev libprotobuf-c-dev libcap-dev libseccomp-dev libyajl-dev go-md2man autoconf python3 automake

curl -LO https://github.com/containers/crun/releases/download/1.19.1/crun-1.19.1-linux-amd64

sudo install -m 755 crun-1.19.1-linux-amd64 /usr/local/sbin/crun

echo -e ${NEWLINEVAR} | sudo tee -a /etc/containerd/config.toml
cat crun_containerd_2x.config | sudo tee -a /etc/containerd/config.toml
sudo systemctl restart containerd.service