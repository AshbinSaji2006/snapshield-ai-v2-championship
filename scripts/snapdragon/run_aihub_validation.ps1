$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$python = Join-Path $root '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python)) { throw 'Create the documented v2 virtual environment first.' }
& $python (Join-Path $PSScriptRoot 'run_aihub_validation.py')
exit $LASTEXITCODE
