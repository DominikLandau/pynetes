#!/bin/bash

### Turn off swap in order for the kubelet to work properly
sudo swapoff -a
sudo sed -ri '/\sswap\s/s/^#?/#/' /etc/fstab


https://kubernetes.io/docs/setup/production-environment/container-runtimes/
### ipv4 forward
#### sysctl params required by setup, params persist across reboots
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF

#### Apply sysctl params without reboot
sudo sysctl --system
