MPT ULTIMATE MANIM COURSE MODE KIT
==================================

This is a scalable foundation for a serious 3Blue1Brown / Apple-keynote style Course Mode.

IMPORTANT:
This is not a 1000-file production engine yet. That would be a large software project.
This kit gives you the correct architecture, folder structure, reusable animation engine modules,
renderers, JSON spec format, and a working demo renderer that can be expanded.

Main idea:
- You manually edit scenes_course.json for any topic.
- The renderer reads the JSON.
- Manim creates animated course clips.
- MoneyPrinterTurbo can assemble voice/subtitles/final video.

Quick run:
1. Extract to C:\MPT_Ultimate_Manim_Course_Mode_Kit
2. cd /d C:\MPT_Ultimate_Manim_Course_Mode_Kit
3. python -m pip install -r requirements.txt
4. copy samples\electricity_advanced.json scenes_course.json
5. render_all.bat
6. Use generated\clips in MoneyPrinterTurbo Local File mode.

Docs:
- docs\ULTIMATE_MANIM_COURSE_ARCHITECTURE.txt
- docs\HOW_TO_RUN.txt
- docs\JSON_SPEC_GUIDE.txt
- docs\ROADMAP_TO_FULL_ENGINE.txt
