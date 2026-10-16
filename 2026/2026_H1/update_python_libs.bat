@echo off
TITLE Update Python Libraries

echo Upgrading pip (the Python package manager) first...
python -m pip install --upgrade pip
echo.
echo ================================================
echo.
echo Checking for outdated packages and upgrading them...
echo.

:: This command lists outdated packages in 'freeze' format (package==version)
:: The FOR loop then splits each line at the '==' sign and takes the first part (the package name)
FOR /F "delims== tokens=1" %%G IN ('pip list --outdated --format=freeze') DO (
    echo Upgrading %%G...
    pip install --upgrade "%%G"
)

echo.
echo ===================================
echo All packages have been updated.
echo ===================================
echo.
pause
