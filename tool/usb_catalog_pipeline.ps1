param([int]$WaitForProcess=0)
$ErrorActionPreference='Stop'
$projectFolder=Split-Path -Parent $PSScriptRoot
$catalogFolder='E:\Icfes_SaberPlus\_SaberPlus_catalogo'
if (-not (Test-Path -LiteralPath $catalogFolder)) { throw 'No esta disponible el catalogo de la USB.' }
if ($WaitForProcess -gt 0) {
    $existing=Get-CimInstance Win32_Process -Filter ('ProcessId = '+$WaitForProcess) -ErrorAction SilentlyContinue
    if ($existing) {
        if ($existing.CommandLine -notmatch 'usb_pdf_catalog.py scan') { throw 'El proceso a esperar no es el escaneo previsto.' }
        Write-Output ('Esperando el inventario activo: ' + $WaitForProcess)
        Wait-Process -Id $WaitForProcess -ErrorAction SilentlyContinue
    }
}
Set-Location -LiteralPath $projectFolder
Write-Output 'FASE: completar escaneo y huellas'
& uv run --with pymupdf python tool/usb_pdf_catalog.py scan
if ($LASTEXITCODE -ne 0) { throw 'Escaneo interrumpido. Reanudar, no continuar borrados.' }
Write-Output 'FASE: eliminar solo duplicados binarios con registro recuperable'
& uv run --with pymupdf python tool/usb_pdf_catalog.py dedup --apply
if ($LASTEXITCODE -ne 0) { throw 'La verificacion de duplicados se detuvo.' }
Write-Output 'FASE: reconocimiento local de texto de PDF unicos'
& uv run --with pymupdf python tool/usb_pdf_catalog.py ocr
if ($LASTEXITCODE -ne 0) { throw 'OCR interrumpido. Conservar el catalogo para reanudar.' }
& uv run --with pymupdf python tool/usb_pdf_catalog.py report
Write-Output 'RECORRIDO AUTOMATICO TERMINADO. Consultar errores y pendientes. La revision semantica y comparacion de variantes siguen pendientes; no equivalen al OCR.'
