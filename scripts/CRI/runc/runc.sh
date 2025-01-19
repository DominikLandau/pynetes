#!/bin/bash

if command -v runc 2>&1 >/dev/null
then
    echo "runc exists"
    exit 0
fi

curl -LO https://github.com/opencontainers/runc/releases/download/v1.2.2/runc.amd64
curl -LO https://github.com/opencontainers/runc/releases/download/v1.2.2/runc.sha256sum
cat runc.sha256sum | grep runc.amd64 | sha256sum --check

sudo install -m 755 runc.amd64 /usr/local/sbin/runc