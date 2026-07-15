from manim import *
from .primitives import txt
from .theme import *

def apple_hello(scene,text,size=62):
    letters=VGroup(*[txt(ch,size,CREAM,BOLD) for ch in str(text)])
    letters.arrange(RIGHT,buff=.015).move_to(UP*.5)
    for ch in letters:
        ch.shift(UP*1.1)
        scene.play(FadeIn(ch), ch.animate.shift(DOWN*1.1), run_time=.035)
    scene.play(Indicate(letters,color=CYAN),run_time=.55)
    return letters

def fade_title(scene,text):
    t=txt(text,52,CREAM,BOLD).to_edge(UP,buff=.32)
    scene.play(FadeIn(t,shift=DOWN),run_time=.55)
    return t
