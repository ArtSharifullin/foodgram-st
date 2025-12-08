helm upgrade redis redis -n foodgram

helm repo add heywood8-helm-charts https://heywood8.github.io/helm-charts/

helm install my-redisinsight heywood8-helm-charts/redisinsight -n foodgram -f redis-insight.yaml --version 0.4.5