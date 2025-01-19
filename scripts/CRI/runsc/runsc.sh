#!/bin/bash

if command -v runsc 2>&1 >/dev/null
then
    echo "runsc exists"
    exit 0
fi

# https://gvisor.dev/docs/user_guide/install/
set -e
ARCH=$(uname -m)
URL=https://storage.googleapis.com/gvisor/releases/release/latest/${ARCH}

wget ${URL}/runsc ${URL}/runsc.sha512 ${URL}/containerd-shim-runsc-v1 ${URL}/containerd-shim-runsc-v1.sha512
sha512sum -c runsc.sha512 -c containerd-shim-runsc-v1.sha512

rm -f *.sha512

chmod a+rx runsc containerd-shim-runsc-v1
sudo mv runsc containerd-shim-runsc-v1 /usr/local/sbin

echo -e ${NEWLINEVAR} | sudo tee -a /etc/containerd/config.toml
cat runsc_containerd_2x.config | sudo tee -a /etc/containerd/config.toml
sudo systemctl restart containerd.service