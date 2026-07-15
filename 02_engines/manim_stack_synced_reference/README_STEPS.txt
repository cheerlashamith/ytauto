MPT MANIM STACK SYNCED KIT
==========================

Purpose:
This kit improves Stack course mode by splitting one big Manim animation into scene-by-scene clips.
This makes narration and visuals easier to sync.

WHAT TO DO
----------

1. Extract this folder to C:\MPT_Manim_Stack_Synced_Kit

2. Open CMD:

   cd /d C:\MPT_Manim_Stack_Synced_Kit

3. Render all Manim scene clips:

   render_all_stack_scenes.bat

4. Concatenate them in correct order:

   concat_stack_scenes.bat

5. Output final ordered visual clip:

   generated\final\stack_ordered_manim.mp4

6. Open MoneyPrinterTurbo.

7. Use settings:

   Video Subject:
   Stack Data Structure Explained for Beginners

   Video Script:
   paste stack_script.txt

   Video Keywords:
   paste stack_keywords.txt

   Video Source:
   Local file

   Upload Local Files:
   generated\final\stack_ordered_manim.mp4

   Transition:
   None

   Aspect Ratio:
   Landscape 16:9

   Maximum Duration:
   120

   TTS:
   Azure TTS V1

   BGM Volume:
   0.05

WHY THIS IS BETTER
------------------
The visual order is fixed because we concatenate clips ourselves.
MoneyPrinterTurbo receives one ordered Manim video.
The script is shorter and follows the same scene order.

LIMITATION
----------
Exact word-level sync is still not perfect because MoneyPrinterTurbo creates TTS separately.
The next step is per-scene TTS duration matching.
