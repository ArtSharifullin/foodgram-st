#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NAMESPACE="${VAULT_NAMESPACE:-vault}"
RELEASE_NAME="${VAULT_RELEASE:-vault}"

REPO_NAME="${VAULT_HELM_REPO_NAME:-itis-charts}"
REPO_URL="${VAULT_HELM_REPO_URL:-https://charts.itis-3k-cloud.ru/}"

helm repo add "${REPO_NAME}" "${REPO_URL}" >/dev/null
helm repo update "${REPO_NAME}" >/dev/null

helm upgrade --install "${RELEASE_NAME}" "${REPO_NAME}/hashicorp/vault" \
  --namespace "${NAMESPACE}" \
  --create-namespace \
  -f "${SCRIPT_DIR}/vault-values.yaml"

kubectl --namespace "${NAMESPACE}" apply -f "${SCRIPT_DIR}/vault-nodeport.yaml"