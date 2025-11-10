# MP3 Splitter Activation Script for PowerShell

Write-Host "🎵 Activating MP3 Splitter Environment..." -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Check if virtual environment exists
if (Test-Path "venv") {
    # Activate virtual environment
    .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "   Run: python -m venv venv" -ForegroundColor Yellow
    Write-Host "   Then run: .\activate.ps1 again" -ForegroundColor Yellow
    exit 1
}

# Setup FFmpeg from project folder
$ffmpegPath = ".\ffmpeg\bin"
if (Test-Path $ffmpegPath) {
    # Add to current session PATH
    $env:Path = "$($PWD.Path)\ffmpeg\bin;$env:Path"
    Write-Host "✅ FFmpeg added to PATH: $ffmpegPath" -ForegroundColor Green
    
    # Test FFmpeg
    try {
        $ffmpegVersion = & ffmpeg -version 2>&1 | Select-Object -First 1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ FFmpeg verified: $ffmpegVersion" -ForegroundColor Green
        } else {
            Write-Host "⚠️  FFmpeg found but not working properly" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠️  Could not verify FFmpeg: $_" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ FFmpeg folder not found at: $ffmpegPath" -ForegroundColor Red
    Write-Host "   Please ensure FFmpeg is in: project\ffmpeg\bin\" -ForegroundColor Yellow
}

# Show status
$pythonVersion = & python --version
Write-Host "`n📊 Environment Status:" -ForegroundColor Cyan
Write-Host "   Python: $pythonVersion" -ForegroundColor White
Write-Host "   Project: MP3 Splitter" -ForegroundColor White
Write-Host "   Ready to use! 🚀" -ForegroundColor Green

Write-Host "`n🎯 Usage:" -ForegroundColor Cyan
Write-Host "   Interactive mode: python main.py" -ForegroundColor White
Write-Host "   Direct mode: python simple_splitter.py ""song.mp3"" 5" -ForegroundColor White

Write-Host "`n🔧 To deactivate: deactivate" -ForegroundColor Yellow