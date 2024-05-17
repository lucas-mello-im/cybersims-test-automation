@echo off
setlocal

REM Verifica se o Python está instalado
echo Searching for Python...
where python > nul 2>&1

REM Se o Python não está instalado, %ERRORLEVEL% será diferente de 0
if %ERRORLEVEL% neq 0 (
    echo Start Python Download
    
    REM Baixar o instalador do Python
    set "python_installer=python-3.10.10-amd64.exe"
    set "download_url=https://www.python.org/ftp/python/3.10.10/%python_installer%"

    echo Baixando Python...
    powershell -Command "Invoke-WebRequest -Uri %download_url% -OutFile %python_installer%"

    REM Executar o instalador do Python de forma silenciosa
    echo Instalando Python...
    %python_installer% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

    REM Verificar se a instalação foi bem-sucedida
    where python >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo Falha na instalação do Python.
        exit /b 1
    ) else (
        echo Python foi instalado com sucesso.
    )
) else (
    echo Python já está instalado.
)

REM Finaliza o script
endlocal

echo Creating Virtual Environment
python -m venv venv
call venv/scripts/activate
pip install requests

python "D:\Cybersims\cybersimsue5\Content\Scripts\main.py"

echo Install complete
pause