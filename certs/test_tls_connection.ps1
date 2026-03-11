#!/usr/bin/env pwsh
# TLS Connection Test Script for Mosquitto

$openssl = "C:\Program Files\OpenSSL-Win64\bin\openssl.exe"
$certDir = Get-Location

Write-Host "Testing TLS connection to localhost:8883..." -ForegroundColor Green
Write-Host "Using certificates from: $certDir" -ForegroundColor Cyan

& $openssl s_client `
  -connect localhost:8883 `
  -CAfile ca_certs.crt `
  -cert server_dir/ec_server_cert.pem `
  -key server_dir/ec_server_private.pem `
  -verify 2
