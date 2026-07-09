
@echo off
cd /d "%~dp0"
call "venv37\Scripts\activate.bat"
python -m streamlit run pages\1_Prediction.py
