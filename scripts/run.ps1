$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $project
Start-Process -FilePath 'python' -ArgumentList @('-m','uvicorn','backend.app.main:app','--host','127.0.0.1','--port','8000') -WorkingDirectory $project -WindowStyle Hidden
Set-Location -LiteralPath (Join-Path $project 'frontend')
npm.cmd run dev
