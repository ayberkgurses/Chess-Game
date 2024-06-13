@echo off

REM Create a virtual environment
python -m venv venv

REM Activate the virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Inform the user
echo Setup complete. To activate the virtual environment, run 'venv\Scripts\activate'.
pause
