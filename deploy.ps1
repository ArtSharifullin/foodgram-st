# deploy.ps1 - Упрощенный деплой для Windows

Write-Host "========================================" -ForegroundColor Green
Write-Host "  Развертывание Foodgram Application" -ForegroundColor Green  
Write-Host "========================================" -ForegroundColor Green

# Загрузка переменных из .env
Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]*?)\s*=\s*(.*?)\s*$') {
        $name = $matches[1]
        $value = $matches[2]
        Set-Item -Path "env:$name" -Value $value
    }
}

Write-Host "`n[1/4] Создание namespaces..." -ForegroundColor Yellow
kubectl create namespace foodgram --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace rabbitmq --dry-run=client -o yaml | kubectl apply -f -

Write-Host "`n[2/4] Установка RabbitMQ..." -ForegroundColor Yellow
helm upgrade --install rabbitmq oci://registry-1.docker.io/cloudpirates/rabbitmq `
    -n rabbitmq --create-namespace `
    -f backend\foodgram\rabbitmq\values.yaml

Write-Host "`nОжидание RabbitMQ (30 сек)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

Write-Host "`n[3/4] Установка Foodgram приложения..." -ForegroundColor Yellow
helm upgrade --install app .\helm\app -n foodgram

Write-Host "`n[4/4] Проверка статуса..." -ForegroundColor Yellow
kubectl get pods -n rabbitmq
kubectl get pods -n foodgram

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  Развертывание завершено!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
