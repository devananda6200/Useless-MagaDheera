@echo off
echo.
echo ========================================
echo    MAGADHEERA IMAGE SETUP TOOL
echo ========================================
echo.
echo Choose your preferred method:
echo.
echo 1. GUI Image Manager (Recommended - Easy drag and drop)
echo 2. Command Line Tool (Text-based)
echo 3. View current images
echo.
set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Starting GUI Image Manager...
    python image_manager.py
) else if "%choice%"=="2" (
    echo.
    echo Starting Command Line Tool...
    python add_custom_images.py
) else if "%choice%"=="3" (
    echo.
    echo Current Images:
    echo.
    echo CHARACTERS:
    dir characters\*.png /b 2>nul || echo No character images found
    echo.
    echo LOVERS:
    dir lovers\*.png /b 2>nul || echo No lover images found
) else (
    echo Invalid choice!
)

echo.
echo.
echo Remember to restart your backend server after adding images:
echo python app.py
echo.
echo Then test at: http://localhost:3000
echo.
pause
