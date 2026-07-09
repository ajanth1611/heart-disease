Set-Location -Path "$PSScriptRoot"
& "$PSScriptRoot\venv37\Scripts\Activate.ps1"
python -m streamlit run pages\1_Prediction.py
