#!/bin/bash

if command -v containerd 2>&1 >/dev/null
then
    echo "Containerd exists"
    exit 0
fi

# Downlaod containerd
curl -LO https://github.com/containerd/containerd/releases/download/v2.0.0/containerd-2.0.0-linux-amd64.tar.gz
curl -LO https://github.com/containerd/containerd/releases/download/v2.0.0/containerd-2.0.0-linux-amd64.tar.gz.sha256sum
cat containerd-2.0.0-linux-amd64.tar.gz.sha256sum | sha256sum --check

sudo tar -xzf containerd-2.0.0-linux-amd64.tar.gz
sudo install -m 755 ./bin/* /usr/local/bin

curl -LO https://raw.githubusercontent.com/containerd/containerd/main/containerd.service
sudo mkdir -p /usr/local/lib/systemd/system/
sudo mv containerd.service /usr/local/lib/systemd/system/containerd.service

sudo systemctl daemon-reload
sudo systemctl enable --now containerd

# https://github.com/containerd/containerd/blob/main/docs/cri/config.md
sudo mkdir -p /etc/containerd
sudo cp containerd_2x.config /etc/containerd/config.toml
sudo systemctl restart containerd.service