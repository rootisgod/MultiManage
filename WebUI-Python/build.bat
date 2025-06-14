@echo off
echo ===== Building MultiManage Executable =====

:: Create a virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Install requirements
echo Installing requirements...
pip install -r requirements-build.txt

:: Run PyInstaller
echo Running PyInstaller...
pyinstaller --clean multimanage.spec

:: Deactivate virtual environment
deactivate

echo ===== Build Complete =====
echo The executable is located in the dist\MultiManage directory
