#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHART_DIR="${SCRIPT_DIR}/app"
VALUES_FILES=(-f "${CHART_DIR}/values.yaml")

if [ -f "${SCRIPT_DIR}/.env" ]; then
  set -a
  # shellcheck disable=SC1090
  source "${SCRIPT_DIR}/.env"
  set +a
fi

if [ -f "${SCRIPT_DIR}/values.vault.yaml" ]; then
  VALUES_FILES+=(-f "${SCRIPT_DIR}/values.vault.yaml")
fi

NAMESPACE="${NAMESPACE:-foodgram}"
RELEASE_NAME="${RELEASE_NAME:-foodgram}"

helm secrets --backend vals upgrade --install "${RELEASE_NAME}" "${CHART_DIR}" \
  --namespace "${NAMESPACE}" \
  --create-namespace \
  "${VALUES_FILES[@]}"

