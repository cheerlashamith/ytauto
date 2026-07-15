from manim import *
from .primitives import txt
from .theme import *

def apple_hello(scene,text,size=62):
    t = Text(str(text), font_size=size, color=CREAM, weight=BOLD).move_to(UP*.5)
    for ch in t:
        ch.shift(UP*1.1)
    if len(t) > 0:
        animations = [AnimationGroup(FadeIn(ch), ch.animate.shift(DOWN*1.1)) for ch in t]
        scene.play(LaggedStart(*animations, lag_ratio=0.05, run_time=max(1.5, len(t)*0.05)))
    scene.play(Indicate(t,color=CYAN),run_time=.55)
    return t

def fade_title(scene,text):
    t=txt(text,52,CREAM,BOLD).to_edge(UP,buff=.32)
    scene.play(FadeIn(t,shift=DOWN),run_time=.55)
    return t
