param(
    [Parameter(Mandatory=$true)][string]$Root,
    [Parameter(Mandatory=$true)][string]$Plan,
    [switch]$Apply,
    [switch]$Undo
)
$ErrorActionPreference = 'Stop'
$targetRoot = (Resolve-Path -LiteralPath $Root).Path.TrimEnd('\')
$renamePlan = Get-Content -LiteralPath $Plan -Raw -Encoding UTF8 | ConvertFrom-Json
if ($renamePlan.root -ne $targetRoot) { throw 'La carpeta no corresponde al registro.' }
$operations = @()
$targetNames = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
foreach ($entry in $renamePlan.files) {
    $fromName = if ($Undo) { $entry.new_name } else { $entry.original }
    $toName = if ($Undo) { $entry.original } else { $entry.new_name }
    if ([System.IO.Path]::GetFileName($fromName) -ne $fromName -or [System.IO.Path]::GetFileName($toName) -ne $toName) { throw 'El registro contiene una ruta no permitida.' }
    $source = [System.IO.Path]::GetFullPath((Join-Path $targetRoot $fromName))
    $destination = [System.IO.Path]::GetFullPath((Join-Path $targetRoot $toName))
    if ([System.IO.Path]::GetDirectoryName($source) -ne $targetRoot -or [System.IO.Path]::GetDirectoryName($destination) -ne $targetRoot) { throw 'Destino fuera de la carpeta autorizada.' }
    if (-not $targetNames.Add($toName)) { throw ('Nombre repetido: ' + $toName) }
    if (Test-Path -LiteralPath $destination) { throw ('El destino ya existe; no se sobrescribira: ' + $toName) }
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw ('Falta el origen: ' + $fromName) }
    if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash.ToLowerInvariant() -ne $entry.sha256) { throw ('El contenido cambio; se cancela: ' + $fromName) }
    $operations += [PSCustomObject]@{Source=$source;Destination=$destination;NewName=$toName;Hash=$entry.sha256}
}
Write-Output ('Verificados: ' + $operations.Count + ' archivos. Modo: ' + $(if ($Apply) {'aplicar'} else {'solo comprobar'}))
if (-not $Apply) { $operations | Select-Object Source,NewName; return }
foreach ($operation in $operations) {
    Rename-Item -LiteralPath $operation.Source -NewName $operation.NewName
    if ((Get-FileHash -LiteralPath $operation.Destination -Algorithm SHA256).Hash.ToLowerInvariant() -ne $operation.Hash) { throw ('Fallo la comprobacion posterior: ' + $operation.NewName) }
    Write-Output ('OK ' + $operation.NewName)
}
Write-Output 'Renombrado completo. Todos los SHA-256 coinciden con el registro original.'
