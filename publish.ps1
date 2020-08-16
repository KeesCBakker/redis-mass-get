$ErrorActionPreference = "Stop"

$env:PIPENV_VERBOSITY = '-1';
git config --global core.safecrlf false

function Print-Header {
    param( [string]$header )
    Write-Host ""
    Write-Host "$header" -ForeGroundColor Yellow
}

function Check-Failed{
    param( [string]$header )
    if($LASTEXITCODE -gt 0){
        Write-Host "$header" -ForegroundColor Red
        Write-Host ""
        exit $LASTEXITCODE
    }
}


Remove-Item build -Recurse -ErrorAction Ignore
Remove-Item dist -Recurse -ErrorAction Ignore

Print-Header "Checking Git status..."
if(git status --porcelain | where {$_ -match '^\?\?'}){
    Write-Host "DIRTY: Untracked files exist. Add and commit them first."
    Write-Host ""
    exit $LASTEXITCODE
} 
elseif(git status --porcelain | where {$_ -notmatch '^\?\?'}) {
    Write-Host "DIRTY: Uncommitted files exist. Commit them first."
    Write-Host ""
    exit $LASTEXITCODE
}

Print-Header "Installing (dev) packages..."
pipenv sync --dev
Check-Failed "Intalling packages failed..."

Print-Header "Testing..."
python -m pytest
Check-Failed "Testing failed..."

Print-Header "Patch version..."
bumpversion patch
Check-Failed "Patching failed..."

Print-Header "Build..."
python setup.py sdist bdist_wheel
Check-Failed "Setup failed..."
twine check dist/*
Check-Failed "Twine check failed..."


Print-Header "Distribute..."
twine upload dist/*
Check-Failed "Distribution failed..."

Write-Host ""
Write-Host "Done" -ForeGroundColor Green
Write-Host ""
