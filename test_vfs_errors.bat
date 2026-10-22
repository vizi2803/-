@echo off
python -m src.main --vfs tests\non_existent_folder
python -m src.main --vfs tests\vfs_minimal\empty.txt
pause