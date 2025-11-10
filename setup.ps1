# MP3 Splitter - PowerShell Setup Script

Write-Host "🎵 MP3 Splitter Environment Setup" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "requirements.txt")) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

# Check Python versions
Write-Host "`nChecking Python versions..." -ForegroundColor Yellow
$pythonVersions = & py --list 2>$null

if (-not $pythonVersions) {
    Write-Host "❌ Python not found. Please install Python 3.11 or later." -ForegroundColor Red
    exit 1
}

Write-Host "Available Python versions:" -ForegroundColor Cyan
$pythonVersions | ForEach-Object { Write-Host "  $_" }

# Check for Python 3.11
$python311 = $pythonVersions -match "3.11"
if ($python311) {
    Write-Host "✅ Found Python 3.11" -ForegroundColor Green
    $pythonCmd = "py -3.11"
} else {
    Write-Host "⚠️  Python 3.11 not found, using default Python 3" -ForegroundColor Yellow
    $pythonCmd = "py -3"
}

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
& $pythonCmd -m venv venv

if (-not (Test-Path "venv")) {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Virtual environment created" -ForegroundColor Green

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Verify activation
if ($env:VIRTUAL_ENV) {
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
    
    # Check Python version in venv
    $venvPythonVersion = & python --version
    Write-Host "Python version in virtual environment: $venvPythonVersion" -ForegroundColor Cyan
} else {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
& python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Test the installation
Write-Host "`nTesting installation..." -ForegroundColor Yellow
try {
    & python -c "from src.mp3_splitter import MP3Splitter; print('✅ MP3 Splitter imported successfully')"
    Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
} catch {
    Write-Host "❌ Setup test failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host "`n🎉 Setup complete! Your environment is ready." -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Always activate the virtual environment: .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. Run the application: python main.py" -ForegroundColor White
Write-Host "3. Install FFmpeg if you haven't already" -ForegroundColor White
Write-Host "`nTo deactivate the virtual environment, run: deactivate" -ForegroundColor Yellow