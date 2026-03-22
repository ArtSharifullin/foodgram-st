helm upgrade --install redis redis -n foodgram

helm repo add heywood8-helm-charts https://heywood8.github.io/helm-charts/

helm upgrade --install my-redisinsight heywood8-helm-charts/redisinsight \
  -n foodgram \
  -f redisinsight-values.yml \
  --version 0.4.5