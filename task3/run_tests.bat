@echo off
pip install pytest
cd tests
python -m pytest -v
pause