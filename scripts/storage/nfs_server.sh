#!/bin/bash

sudo apt update
sudo apt install nfs-kernel-server nfs-common

sudo mkdir /var/nfs/kubernetes -p
sudo chown nobody:nogroup /var/nfs/kubernetes

sudo nano /etc/exports
# /var/nfs/kubernetes *(rw,sync,subtree_check)
sudo systemctl restart nfs-kernel-server
sudo systemctl status nfs-kernel-server

sudo exportfs -a