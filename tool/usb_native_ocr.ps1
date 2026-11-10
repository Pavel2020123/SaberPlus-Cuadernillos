param([Parameter(Mandatory=$true)][string]$InputFolder,[Parameter(Mandatory=$true)][string]$OutputFile)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null=[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null=[Windows.Graphics.Imaging.BitmapDecoder,Windows.Graphics.Imaging,ContentType=WindowsRuntime]
$null=[Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime]
$asyncMethod=[System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1
function Await-WinRT($Operation,$Type) {
    $task=$asyncMethod.MakeGenericMethod($Type).Invoke($null,@($Operation))
    $task.Wait()
    return $task.Result
}
$engine=[Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if ($null -eq $engine) { throw 'No hay un reconocedor local instalado.' }
$completed=@{}
if (Test-Path -LiteralPath $OutputFile) {
    Get-Content -LiteralPath $OutputFile -Encoding UTF8 | ForEach-Object { try { $old=$_ | ConvertFrom-Json; if (-not $old.error) {$completed[[string]$old.page]=$true} } catch {} }
}
$utf8=New-Object System.Text.UTF8Encoding($false)
$writer=New-Object System.IO.StreamWriter($OutputFile,$true,$utf8)
try {
    foreach ($image in Get-ChildItem -LiteralPath $InputFolder -File -Filter '*.png' | Sort-Object Name) {
        $page=[int]$image.BaseName
        if ($completed.ContainsKey([string]$page)) { continue }
        $stream=$null;$bitmap=$null
        try {
            $file=Await-WinRT ([Windows.Storage.StorageFile]::GetFileFromPathAsync($image.FullName)) ([Windows.Storage.StorageFile])
            $stream=Await-WinRT ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
            $decoder=Await-WinRT ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
            $bitmap=Await-WinRT ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
            $result=Await-WinRT ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
            $lines=@($result.Lines | ForEach-Object { $_.Text })
            $record=@{page=$page;text=($lines -join "`n");error=$null}
        } catch { $record=@{page=$page;text='';error=$_.Exception.Message} }
        finally {if ($bitmap) {$bitmap.Dispose()};if ($stream) {$stream.Dispose()}}
        $writer.WriteLine(($record | ConvertTo-Json -Compress -Depth 4));$writer.Flush()
    }
} finally {$writer.Dispose()}
