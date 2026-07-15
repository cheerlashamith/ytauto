@echo off
cd /d %~dp0
echo Installing backend requirements...
python -m pip install -r backend\requirements.txt
echo.
echo Installing story mode engine requirements...
python -m pip install -r engines\story_mode\requirements.txt
echo.
echo Installing manim course mode requirements...
python -m pip install -r engines\manim_course_mode\requirements.txt
echo.
echo Done. Now run run.bat
pause
