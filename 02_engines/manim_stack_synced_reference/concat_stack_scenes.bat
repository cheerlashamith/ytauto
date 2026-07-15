@echo off
cd /d %~dp0
if not exist generated\final mkdir generated\final
(
echo file '../clips/scene_01_intro.mp4'
echo file '../clips/scene_02_lifo.mp4'
echo file '../clips/scene_03_push.mp4'
echo file '../clips/scene_04_pop.mp4'
echo file '../clips/scene_05_peek.mp4'
echo file '../clips/scene_06_uses.mp4'
echo file '../clips/scene_07_summary.mp4'
) > generated\final\stack_concat_list.txt
ffmpeg -y -f concat -safe 0 -i generated\final\stack_concat_list.txt -c copy generated\final\stack_ordered_manim.mp4
echo.
echo DONE. Final ordered Manim video:
echo generated\final\stack_ordered_manim.mp4
pause
