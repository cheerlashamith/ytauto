from manim import *
from engine.primitives import *
from engine.theme import *

def label(x): return str(x.get('label') if isinstance(x,dict) else x)
def color(x,d=CYAN): return resolve_color(x.get('color') if isinstance(x,dict) else None,d)

def flowchart(scene,vd):
    nodes=vd.get('nodes') or ['Start','Process','Result']; nodes=nodes[:6]
    group=VGroup(*[glow_circle(label(n),color(n)) for n in nodes]).arrange(RIGHT,buff=.42).move_to(ORIGIN)
    scene.play(FadeIn(group[0],scale=.8),run_time=.35)
    for i in range(1,len(group)):
        arr=Arrow(group[i-1].get_right(),group[i].get_left(),buff=.12,color=CYAN,stroke_width=5)
        dot=Dot(group[i-1].get_right(),color=YELLOW,radius=.055)
        scene.play(GrowArrow(arr),FadeIn(group[i],scale=.8),run_time=.42)
        scene.play(MoveAlongPath(dot,arr),run_time=.32); scene.remove(dot)

def process(scene,vd):
    steps=vd.get('steps') or vd.get('nodes') or ['Input','Process','Output']; steps=steps[:5]
    group=VGroup(*[rounded_box(label(s),width=2.1 if len(steps)<=4 else 1.7,color=color(s)) for s in steps]).arrange(RIGHT,buff=.45 if len(steps)<=4 else .25).move_to(ORIGIN)
    scene.play(FadeIn(group[0],shift=UP),run_time=.35)
    for i in range(1,len(group)):
        scene.play(GrowArrow(Arrow(group[i-1].get_right(),group[i].get_left(),buff=.14,color=CYAN,stroke_width=5)),FadeIn(group[i],shift=UP),run_time=.42)

def timeline(scene,vd):
    stops=vd.get('stops') or vd.get('steps') or ['Step 1','Step 2','Step 3']; stops=stops[:6]
    xs=[-5.8+11.6*i/max(1,len(stops)-1) for i in range(len(stops))]
    scene.play(Create(Line([xs[0],0,0],[xs[-1],0,0],color=CYAN,stroke_width=5)),run_time=.6)
    for x,s in zip(xs,stops):
        d=Dot([x,0,0],color=GREEN,radius=.09); lab=txt(label(s),22).next_to(d,UP,buff=.25)
        scene.play(FadeIn(d,scale=1.5),FadeIn(lab,shift=UP),run_time=.35)

def comparison(scene,vd):
    left=rounded_box(vd.get('left_title','Before'),3.5,color=ORANGE).shift(LEFT*3.25+UP*.9)
    right=rounded_box(vd.get('right_title','After'),3.5,color=GREEN).shift(RIGHT*3.25+UP*.9)
    scene.play(Create(Line(UP*2,DOWN*2.2,color=VIOLET,stroke_width=3).set_opacity(.65)),FadeIn(left,shift=RIGHT),FadeIn(right,shift=LEFT),run_time=.7)
    l=VGroup(*[txt('• '+str(x),25) for x in vd.get('left_items',['Old'])[:4]]).arrange(DOWN,aligned_edge=LEFT).next_to(left,DOWN,buff=.35)
    r=VGroup(*[txt('• '+str(x),25) for x in vd.get('right_items',['New'])[:4]]).arrange(DOWN,aligned_edge=LEFT).next_to(right,DOWN,buff=.35)
    scene.play(FadeIn(l,shift=UP),FadeIn(r,shift=UP),run_time=.6)

def network(scene,vd):
    center=glow_circle(vd.get('center_label') or vd.get('center') or 'Center',VIOLET).move_to(ORIGIN)
    scene.play(FadeIn(center,scale=.85),run_time=.45)
    nodes=(vd.get('nodes') or ['A','B','C','D'])[:6]
    pos=[LEFT*4+UP*1.7,RIGHT*4+UP*1.7,LEFT*4+DOWN*1.7,RIGHT*4+DOWN*1.7,UP*2.35,DOWN*2.35]
    for n,p in zip(nodes,pos):
        m=rounded_box(label(n),2.1,color=color(n)).move_to(p)
        scene.play(GrowArrow(Arrow(center.get_center(),m.get_center(),buff=.95,color=CYAN,stroke_width=4)),FadeIn(m,scale=.9),run_time=.35)

def equation(scene,vd):
    obj=txt(vd.get('equation','A = B + C'),42,CREAM,BOLD).move_to(ORIGIN)
    scene.play(Write(obj),Create(SurroundingRectangle(obj,color=VIOLET,buff=.32,stroke_width=4)),run_time=1.1)
    scene.play(Indicate(obj,color=YELLOW),run_time=.8)

def cycle(scene,vd):
    steps=(vd.get('steps') or ['A','B','C','D'])[:6]; mobs=[]; radius=2
    for i,s in enumerate(steps):
        a=TAU*i/len(steps); m=rounded_box(s,1.8).move_to([radius*np.cos(a),radius*np.sin(a),0]); mobs.append(m)
    scene.play(*[FadeIn(m,scale=.9) for m in mobs])
    for i in range(len(mobs)): scene.play(GrowArrow(Arrow(mobs[i].get_center(),mobs[(i+1)%len(mobs)].get_center(),buff=.8,color=CYAN)),run_time=.22)

def array(scene,vd):
    vals=(vd.get('values') or [2,5,8,12,16,23,38])[:10]; h=int(vd.get('highlight',len(vals)//2))
    g=VGroup(*[rounded_box(v,1.05,.7) for v in vals]).arrange(RIGHT,buff=.1).move_to(ORIGIN)
    scene.play(FadeIn(g),run_time=.6)
    if 0<=h<len(g): scene.play(Indicate(g[h],color=YELLOW),run_time=.8)
