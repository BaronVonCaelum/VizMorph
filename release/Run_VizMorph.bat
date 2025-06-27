@echo off
echo Starting VizMorph - Tableau Visualization Suggester...
echo.

REM Check if VizMorph.exe exists
if not exist "VizMorph.exe" (
    echo ERROR: VizMorph.exe not found in current directory!
    echo Please ensure all files are in the same folder.
    pause
    exit /b 1
)

REM Launch VizMorph
start "VizMorph" "VizMorph.exe"

REM Optional: Keep window open for debugging
REM echo VizMorph launched successfully!
REM pause
