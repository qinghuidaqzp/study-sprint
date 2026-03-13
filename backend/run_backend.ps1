param(
    [int]$Port = 8000,
    [switch]$UseSqlite,
    [string]$PythonPath = ""
)

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

if (-not $PythonPath) {
    $preferredPython = 'C:\Users\quzhenpeng\AppData\Local\Programs\Python\Python311\python.exe'
    if (Test-Path $preferredPython) {
        $PythonPath = $preferredPython
    } else {
        $PythonPath = 'python'
    }
}

if ($UseSqlite) {
    $env:DATABASE_URL = 'sqlite:///E:/Dasan/appthird/backend/study_sprint.db'
}

& $PythonPath -m uvicorn app.main:app --reload --port $Port