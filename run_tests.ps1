param (
    [string]$Browser = "chrome",
    [switch]$Headless = $false,
    [string]$Marker = "",
    [switch]$OpenReport = $true
)

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "  Selenium WebDriver with Python - Capstone Test Suite Execution" -ForegroundColor Yellow
Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Browser  : $Browser"
Write-Host "Headless : $Headless"
Write-Host "Marker   : $(if ($Marker) { $Marker } else { 'All' })"
Write-Host "===============================================================================" -ForegroundColor Cyan

$argsList = @("-v", "-s", "--browser=$Browser")

if ($Headless) {
    $argsList += "--headless"
}

if ($Marker) {
    $argsList += "-m", $Marker
}

$argsList += "--html=reports/report.html", "--self-contained-html"

Write-Host "`nExecuting command: python -m pytest $($argsList -join ' ')`n" -ForegroundColor Green
python -m pytest @argsList

if ($OpenReport -and (Test-Path "reports/report.html")) {
    Write-Host "`nOpening reports/report.html in default browser..." -ForegroundColor Cyan
    Start-Process "reports/report.html"
}
