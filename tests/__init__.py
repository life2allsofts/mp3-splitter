"""
MP3 Splitter - Professional Audio File Segmentation Tool
Self-Configuring Version - No Manual Updates Required

Developer: Isaac Tetteh-Apotey
Background: Geomatics Engineer & Software Engineering Student
Institution: Quantic School of Business and Technology
"""

__version__ = "2.0.0"
__author__ = "Isaac Tetteh-Apotey"
__email__ = "life2allsofts@gmail.com"
__description__ = "Self-configuring MP3 file splitting tool"

# Auto-run self-test on package import
try:
    from src.self_test import run_self_test
    run_self_test()
except ImportError:
    print("⚠️  Self-test module not available")