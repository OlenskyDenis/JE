# PowerShell wrapper for JE Healthcheck and Quality Gate Runner
param(
    [switch]$Quick,
    [switch]$Full,
    [switch]$E2E,
    [switch]$Mypy,
    [switch]$Fix,
    [switch]$Format,
    [switch]$NoLint
)

$scriptPath = Join-Path $PSScriptRoot "check_all.py"
$pyArgs = @()

if ($Quick) { $pyArgs += "--quick" }
if ($Full) { $pyArgs += "--full" }
if ($E2E) { $pyArgs += "--e2e" }
if ($Mypy) { $pyArgs += "--mypy" }
if ($Fix) { $pyArgs += "--fix" }
if ($Format) { $pyArgs += "--format" }
if ($NoLint) { $pyArgs += "--no-lint" }
if ($args) { $pyArgs += $args }


python $scriptPath @pyArgs
exit $LASTEXITCODE
