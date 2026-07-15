from manim import *
from .theme import *

def txt(text, size=32, color=CREAM, weight=NORMAL):
    s=str(text)
    if len(s)>54: s=s[:51]+"..."
    return Text(s,font_size=size,color=color,weight=weight)

def title(text): return txt(text,52,CREAM,BOLD).to_edge(UP,buff=.32)

def rounded_box(label,width=2.5,height=.78,color=CYAN,fill=PANEL):
    r=RoundedRectangle(width=width,height=height,corner_radius=.12,stroke_color=color,stroke_width=4,fill_color=fill,fill_opacity=.94)
    t=txt(label,25,WHITE,BOLD).move_to(r.get_center())
    return VGroup(r,t)

def glow_circle(label,color=CYAN,radius=.62):
    c=Circle(radius=radius,stroke_color=color,stroke_width=5,fill_color=PANEL,fill_opacity=.94)
    t=txt(label,22,WHITE,BOLD).move_to(c.get_center())
    return VGroup(c,t)

def bullet_group(bullets):
    items=[str(b) for b in (bullets or [])[:4] if str(b).strip()] or ["Key idea","Visual step","Summary"]
    g=VGroup(*[txt("• "+i,25,CREAM) for i in items]).arrange(DOWN,aligned_edge=LEFT,buff=.16)
    return g.to_corner(DL, buff=1.2)

def background_grid(scene):
    grid=VGroup()
    for x in [i*.5 for i in range(-16,17)]:
        if abs(x)<.001: continue
        grid.add(Line([x,-4.5,0],[x,4.5,0],stroke_color="#111827",stroke_width=1,stroke_opacity=.30))
    for y in [i*.5 for i in range(-9,10)]:
        if abs(y)<.001: continue
        grid.add(Line([-8,y,0],[8,y,0],stroke_color="#111827",stroke_width=1,stroke_opacity=.30))
    scene.add(grid)

def particle_field(scene,count=18):
    dots=VGroup()
    for i in range(count):
        x=-7.5+(15*((i*37)%100)/100); y=-4+(8*((i*53)%100)/100)
        dots.add(Dot([x,y,0],radius=.025,color=CYAN).set_opacity(.32))
    scene.add(dots)
