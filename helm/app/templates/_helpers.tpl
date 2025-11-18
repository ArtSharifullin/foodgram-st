{{/*
Expand the name of the chart.
*/}}
{{- define "app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Return backend service name from top-level values with a safe default
*/}}
{{- define "app.backendServiceName" -}}
{{- if and .Values.ingress .Values.ingress.spec .Values.ingress.spec.rules .Values.ingress.spec.rules.host .Values.ingress.spec.rules.host.paths .Values.ingress.spec.rules.host.paths.apiAdminService -}}
  {{- .Values.ingress.spec.rules.host.paths.apiAdminService.name -}}
{{- else -}}
  backend-service
{{- end -}}
{{- end -}}

{{/*
Return backend service name or empty (for conditional fallback in subcharts)
*/}}
{{- define "app.backendServiceNameOrEmpty" -}}
{{- if and .Values.ingress .Values.ingress.spec .Values.ingress.spec.rules .Values.ingress.spec.rules.host .Values.ingress.spec.rules.host.paths .Values.ingress.spec.rules.host.paths.apiAdminService -}}
  {{- .Values.ingress.spec.rules.host.paths.apiAdminService.name -}}
{{- else -}}
  {{- "" -}}
{{- end -}}
{{- end -}}

{{/*
Return nginx service name or empty (for conditional fallback in subcharts)
*/}}
{{- define "app.nginxServiceNameOrEmpty" -}}
{{- if and .Values.ingress .Values.ingress.spec .Values.ingress.spec.rules .Values.ingress.spec.rules.host .Values.ingress.spec.rules.host.paths .Values.ingress.spec.rules.host.paths.slashService -}}
  {{- .Values.ingress.spec.rules.host.paths.slashService.name -}}
{{- else -}}
  {{- "" -}}
{{- end -}}
{{- end -}}

{{/*
Return DB secrets name from top-level values with a safe default
*/}}
{{- define "app.dbSecretsName" -}}
{{- if and .Values.global .Values.global.secret .Values.global.secret.db -}}
  {{- .Values.global.secret.db -}}
{{- else -}}
  db-secrets
{{- end -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "app.labels" -}}
helm.sh/chart: {{ include "app.chart" . }}
{{ include "app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "app.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
