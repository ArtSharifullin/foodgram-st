#!/bin/bash

set -a
source .env
set +a


helm secrets --evaluate-templates --backend vals \
    upgrade --install \
    rabbitmq oci://registry-1.docker.io/cloudpirates/rabbitmq \
    -n rabbitmq --create-namespace \
    -f values.yaml