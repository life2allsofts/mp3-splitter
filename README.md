# MP3 Splitter 🎵

A professional Python tool for splitting MP3 files into multiple parts with precise timing and quality preservation.

## 🚀 About

**Developer**: Isaac Tetteh-Apotey  
**Background**: Land Surveyor (Geomatics Engineer) & Software Engineering Student  
**Institution**: Quantic School of Business and Technology  
**Vision**: Bridging Geomatics Engineering and Software Engineering

## 📋 Features

- **Precise Splitting**: Split MP3 files into exact number of parts
- **Quality Preservation**: Maintain original audio quality
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **User-Friendly**: Both interactive and command-line interfaces
- **Professional**: Built with software engineering best practices

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- FFmpeg (included in project)

### Quick Start
```powershell
# Clone repository
git clone https://github.com/life2allsofts/mp3-splitter.git
cd mp3-splitter

# Activate environment (PowerShell)
.\activate.ps1

# Run interactive mode
python main.py
Manual Setup
powershell
# Create virtual environment
py -3.11 -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
🎯 Usage
Interactive Mode
powershell
python main.py
Command Line Mode
powershell
python simple_splitter.py "audio_file.mp3" 5
🏗️ Architecture
text
src/
├── config.py      # FFmpeg configuration
├── utils.py       # Utility functions
└── mp3_splitter.py # Main splitting logic
📊 Technical Details
Audio Processing: pydub with FFmpeg backend

Precision: Millisecond-level timing accuracy

Format: MP3 quality preservation

Performance: Efficient memory usage for large files

🤝 Contributing
This project demonstrates the integration of:

Geomatics Precision in audio segmentation

Software Engineering principles in development

Business Technology applications

📄 License
MIT License - see LICENSE file for details

👨‍💻 Developer
Isaac Tetteh-Apotey
Geomatics Engineer & Software Engineering Student
Quantic School of Business and Technology

Bridging spatial data precision with software innovation

text

### 2. `LICENSE`
```text
MIT License

Copyright (c) 2024 Isaac Tetteh-Apotey

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.