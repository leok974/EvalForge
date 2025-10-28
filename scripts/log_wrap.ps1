param(
  [Parameter(Mandatory=$true)][string]$cmd,
  [string]$tag = "generic",
  [string]$art = ""
)

$ErrorActionPreference = "SilentlyContinue"
$Info = [ordered]@{}
$now = [DateTime]::UtcNow.ToString("o")
$logDir = Join-Path $PSScriptRoot "..\logs"
$newItem = New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$stdoutPath = [System.IO.Path]::GetTempFileName()
$stderrPath = [System.IO.Path]::GetTempFileName()

# Run the command
$startInfo = New-Object System.Diagnostics.ProcessStartInfo
$startInfo.FileName = "pwsh"
$startInfo.Arguments = "-NoLogo -NoProfile -Command `$ErrorActionPreference='Continue'; $cmd"
$startInfo.RedirectStandardOutput = $true
$startInfo.RedirectStandardError = $true
$startInfo.UseShellExecute = $false
$startInfo.CreateNoWindow = $true

$proc = New-Object System.Diagnostics.Process
$proc.StartInfo = $startInfo
$null = $proc.Start()
$stdOut = $proc.StandardOutput.ReadToEnd()
$stdErr = $proc.StandardError.ReadToEnd()
$proc.WaitForExit()

Set-Content -Path $stdoutPath -Value $stdOut
Set-Content -Path $stderrPath -Value $stdErr

# Basic fingerprint of the failure
$fingerprint = ""
if ($proc.ExitCode -ne 0) {
  $fingerprint = (Get-FileHash -Algorithm SHA1 -InputStream ([IO.MemoryStream]::new([Text.Encoding]::UTF8.GetBytes($stdErr)))).Hash
}

# Optionally load artifact JSON (e.g., coverage)
$artifactJson = $null
if ($art -ne "" -and (Test-Path $art)) {
  try { $artifactJson = Get-Content $art -Raw | ConvertFrom-Json } catch {}
}

$record = [ordered]@{
  ts           = $now
  os           = "windows"
  tag          = $tag
  cwd          = (Get-Location).Path
  command      = $cmd
  exit_code    = $proc.ExitCode
  fingerprint  = $fingerprint
  stdout_tail  = ($stdOut | Select-Object -Last 50)
  stderr_tail  = ($stdErr | Select-Object -Last 50)
  artifact     = if ($artifactJson) { $artifactJson } else { $null }
  quest_id     = $env:QUEST_ID
}

# Append as NDJSON
$journal = Join-Path $logDir "error-journal.ndjson"
($record | ConvertTo-Json -Depth 6 -Compress) + "`n" | Out-File -FilePath $journal -Append -Encoding utf8

# Mirror command output to console
$stdOut
$stdErr | Write-Host -ForegroundColor Red

exit $proc.ExitCode
