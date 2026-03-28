# Task 2 checks: nanobot Up, Flutter main.dart.js, optional WebSocket.
# Usage: .\scripts\verify-task2.ps1  (from repo root)
param(
    [string]$EnvFile = ".env.docker.secret"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

if (-not (Test-Path $EnvFile)) {
    Write-Output "FAIL: missing $EnvFile (copy from .env.docker.example)"
    exit 1
}

$gatewayPort = "42002"
Get-Content $EnvFile | ForEach-Object {
    if ($_ -match '^\s*GATEWAY_HOST_PORT\s*=\s*(.+)$') { $gatewayPort = $Matches[1].Trim() }
}
$accessKey = ""
Get-Content $EnvFile | ForEach-Object {
    if ($_ -match '^\s*NANOBOT_ACCESS_KEY\s*=\s*(.+)$') { $accessKey = $Matches[1].Trim().Trim('"') }
}
if ([string]::IsNullOrWhiteSpace($accessKey)) {
    Write-Output "FAIL: NANOBOT_ACCESS_KEY is empty in $EnvFile"
    exit 1
}

$ps = docker compose --env-file $EnvFile ps -a 2>&1 | Out-String
if ($ps -notmatch 'nanobot') {
    Write-Output "FAIL: no nanobot service in compose ps"
    exit 1
}
if ($ps -notmatch '(?i)\sUp\s') {
    Write-Output "FAIL: nanobot container not Up (docker compose --env-file $EnvFile ps -a)"
    exit 1
}

$u = "http://127.0.0.1:${gatewayPort}/flutter/main.dart.js"
try {
    $r = Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 15
    if ($r.Content.Length -lt 10) { throw "short body" }
} catch {
    Write-Output "FAIL: Flutter bundle missing at $u"
    exit 1
}

if (Get-Command websocat -ErrorAction SilentlyContinue) {
    Write-Output "SKIP: WebSocket (install websocat and test ws://127.0.0.1:${gatewayPort}/ws/chat manually)"
} else {
    Write-Output "SKIP: websocat not on PATH"
}

Write-Output "PASS"
