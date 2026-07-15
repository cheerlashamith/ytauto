import json, os
from manim import *
from engine.primitives import background_grid, particle_field, bullet_group
from engine.text_effects import fade_title, apple_hello
from renderers.basic import *
from engine.theme import BG, VIOLET
config.background_color=BG; config.pixel_width=1920; config.pixel_height=1080; config.frame_width=16; config.frame_height=9
class UltimateCourseScene(Scene):
    def construct(self):
        data=json.load(open('scenes_course.json',encoding='utf-8')); idx=int(os.environ.get('SCENE_INDEX','0')); sc=data['scenes'][idx]
        background_grid(self); particle_field(self,22)
        dt=str(sc.get('diagram_type','generic')).lower(); vd=sc.get('visual_data',{}) if isinstance(sc.get('visual_data',{}),dict) else {}
        if dt=='title_card':
            main=vd.get('main_title') or vd.get('main_message') or data.get('meta',{}).get('title') or sc.get('title','Course')
            apple_hello(self,main,56); sub=vd.get('subtitle') or vd.get('secondary_message') or data.get('meta',{}).get('subtitle')
            if sub: self.play(FadeIn(txt(sub,32,VIOLET).next_to(VGroup(*self.mobjects),DOWN,buff=.25)),run_time=.6)
            self.wait(1.1); return
        fade_title(self,sc.get('title','Scene'))
        if dt in ['flowchart','motion_flowchart','electric_grid']: flowchart(self,vd)
        elif dt=='process': process(self,vd)
        elif dt=='timeline': timeline(self,vd)
        elif dt=='comparison': comparison(self,vd)
        elif dt=='network': network(self,vd)
        elif dt=='equation': equation(self,vd)
        elif dt=='probability': process(self,{'steps':[vd.get('prior','Prior'),vd.get('evidence','Evidence'),vd.get('posterior','Posterior')]})
        elif dt=='cycle': cycle(self,vd)
        elif dt=='array': array(self,vd)
        else: process(self,{'steps':sc.get('bullets') or ['Idea','Example','Result']})
        self.play(FadeIn(bullet_group(sc.get('bullets',[])),shift=UP),run_time=.5); self.wait(1)
