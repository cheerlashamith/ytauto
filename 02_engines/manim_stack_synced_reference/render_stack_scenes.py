from manim import *

# 3Blue1Brown-inspired serious course style.
# Landscape 16:9 is best for course explanation.
config.background_color = "#05070D"
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9

CREAM = "#DEDBC8"
CYAN = "#6EE7D8"
GREEN = "#72EDA7"
VIOLET = "#A98BFF"
YELLOW = "#F7D774"
RED = "#FF6B73"
BLUE_DARK = "#0B1833"
PANEL = "#07111F"


def title_text(text):
    return Text(text, color=CREAM, font_size=46, weight=BOLD).to_edge(UP)


def subtitle_text(text):
    return Text(text, color=VIOLET, font_size=26).next_to(title_text(" "), DOWN)


def make_stack_frame():
    left = Line(LEFT*1.55 + DOWN*2.25, LEFT*1.55 + UP*1.65, color=CYAN, stroke_width=6)
    right = Line(RIGHT*1.55 + DOWN*2.25, RIGHT*1.55 + UP*1.65, color=CYAN, stroke_width=6)
    bottom = Line(LEFT*1.55 + DOWN*2.25, RIGHT*1.55 + DOWN*2.25, color=CYAN, stroke_width=6)
    return VGroup(left, right, bottom)


def stack_item(value, y=0, width=2.55):
    rect = RoundedRectangle(width=width, height=0.55, corner_radius=0.08,
                            stroke_color=CYAN, stroke_width=4,
                            fill_color=BLUE_DARK, fill_opacity=0.95)
    txt = Text(str(value), color=GREEN, font_size=30, weight=BOLD)
    return VGroup(rect, txt).move_to([0, y, 0])


def top_arrow(y):
    arr = Arrow(RIGHT*3.0 + UP*y, RIGHT*1.62 + UP*y, color=GREEN, buff=0, stroke_width=6)
    lab = Text("TOP", color=GREEN, font_size=28, weight=BOLD).next_to(arr, RIGHT, buff=0.16)
    return VGroup(arr, lab)


def bottom_caption(text):
    box = RoundedRectangle(width=12.8, height=0.8, corner_radius=0.14,
                           stroke_color=rgba_to_color([1,1,1,0.15]),
                           fill_color="#000000", fill_opacity=0.42)
    t = Text(text, color=CREAM, font_size=28)
    g = VGroup(box, t).to_edge(DOWN, buff=0.35)
    return g


def small_code(lines):
    rendered = VGroup(*[Text(line, color=CREAM, font_size=25, font="Consolas") for line in lines])
    rendered.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    bg = RoundedRectangle(width=5.8, height=max(1.2, 0.48*len(lines)+0.55), corner_radius=0.18,
                          stroke_color=VIOLET, stroke_width=2,
                          fill_color="#070912", fill_opacity=0.92)
    bg.move_to(rendered.get_center())
    return VGroup(bg, rendered)


class StackBase(Scene):
    def setup_scene(self, title, subtitle=None):
        self.camera.background_color = "#05070D"
        bg_grid = NumberPlane(
            x_range=[-8, 8, 1], y_range=[-4.5, 4.5, 1],
            background_line_style={"stroke_color": "#1A2130", "stroke_width": 1, "stroke_opacity": 0.22}
        )
        self.add(bg_grid)
        t = title_text(title)
        self.play(FadeIn(t, shift=DOWN), run_time=0.7)
        if subtitle:
            st = Text(subtitle, color=VIOLET, font_size=26).next_to(t, DOWN, buff=0.12)
            self.play(Write(st), run_time=0.7)
            return t, st
        return t, None


class StackScene01Intro(StackBase):
    def construct(self):
        self.setup_scene("What is a Stack?", "A vertical data structure")
        frame = make_stack_frame()
        label = Text("STACK", color=CREAM, font_size=30).next_to(frame, DOWN)
        explain = VGroup(
            Text("A stack stores items", color=CREAM, font_size=30),
            Text("one above another", color=CREAM, font_size=30),
            Text("like a pile of plates", color=CYAN, font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT).shift(DOWN*0.2)
        self.play(Create(frame), FadeIn(label), run_time=1.0)
        self.play(FadeIn(explain, shift=RIGHT), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(explain), run_time=0.5)
        cap = bottom_caption("A stack keeps items in a vertical order.")
        self.play(FadeIn(cap, shift=UP), run_time=0.6)
        self.wait(1.4)


class StackScene02LIFO(StackBase):
    def construct(self):
        self.setup_scene("LIFO Rule", "Last In, First Out")
        frame = make_stack_frame()
        self.play(Create(frame), run_time=0.7)
        ys = [-1.85, -1.22, -0.59]
        vals = [10, 20, 30]
        items = []
        for v, y in zip(vals, ys):
            it = stack_item(v, y).shift(UP*3.3)
            self.play(it.animate.shift(DOWN*3.3), run_time=0.65)
            items.append(it)
        top = top_arrow(ys[-1])
        self.play(FadeIn(top, shift=LEFT), run_time=0.6)
        cap = bottom_caption("The last value pushed is the first value removed.")
        self.play(FadeIn(cap, shift=UP), run_time=0.6)
        self.play(Indicate(items[-1], color=YELLOW), run_time=1.0)
        self.wait(1.2)


class StackScene03Push(StackBase):
    def construct(self):
        self.setup_scene("Push Operation", "Add a new item to the top")
        frame = make_stack_frame()
        existing = VGroup(stack_item(10, -1.85), stack_item(20, -1.22))
        self.play(Create(frame), FadeIn(existing), run_time=0.8)
        new = stack_item(30, -0.59).shift(UP*3.2)
        code = small_code(["push(30)", "top = 30"]).to_edge(RIGHT).shift(UP*0.3)
        self.play(FadeIn(code, shift=LEFT), run_time=0.6)
        self.play(new.animate.shift(DOWN*3.2), run_time=1.0)
        top = top_arrow(-0.59)
        self.play(FadeIn(top, shift=LEFT), Indicate(new, color=GREEN), run_time=0.8)
        cap = bottom_caption("Push places the new item above the previous top.")
        self.play(FadeIn(cap, shift=UP), run_time=0.6)
        self.wait(1.1)


class StackScene04Pop(StackBase):
    def construct(self):
        self.setup_scene("Pop Operation", "Remove the top item")
        frame = make_stack_frame()
        ys = [-1.85, -1.22, -0.59]
        items = VGroup(stack_item(10, ys[0]), stack_item(20, ys[1]), stack_item(30, ys[2]))
        top = top_arrow(ys[2])
        self.play(Create(frame), FadeIn(items), FadeIn(top), run_time=0.8)
        code = small_code(["pop()", "removed = 30", "top = 20"]).to_edge(RIGHT).shift(UP*0.2)
        self.play(FadeIn(code, shift=LEFT), run_time=0.6)
        self.play(items[2].animate.shift(UP*3.0).set_opacity(0), FadeOut(top), run_time=1.0)
        new_top = top_arrow(ys[1])
        self.play(FadeIn(new_top, shift=LEFT), Indicate(items[1], color=YELLOW), run_time=0.8)
        cap = bottom_caption("Pop removes only the top item.")
        self.play(FadeIn(cap, shift=UP), run_time=0.6)
        self.wait(1.0)


class StackScene05Peek(StackBase):
    def construct(self):
        self.setup_scene("Peek Operation", "Read top without removing it")
        frame = make_stack_frame()
        ys = [-1.85, -1.22, -0.59]
        items = VGroup(stack_item(10, ys[0]), stack_item(20, ys[1]), stack_item(30, ys[2]))
        top = top_arrow(ys[2])
        self.play(Create(frame), FadeIn(items), FadeIn(top), run_time=0.8)
        glow = SurroundingRectangle(items[2], color=VIOLET, buff=0.08, stroke_width=6)
        code = small_code(["peek()", "returns 30", "stack unchanged"]).to_edge(RIGHT).shift(UP*0.2)
        self.play(FadeIn(code, shift=LEFT), Create(glow), run_time=0.9)
        cap = bottom_caption("Peek checks the top value, but the stack remains the same.")
        self.play(FadeIn(cap, shift=UP), run_time=0.6)
        self.wait(1.3)


class StackScene06Uses(StackBase):
    def construct(self):
        self.setup_scene("Where Stacks Are Used", "Real programming examples")
        center = Dot(ORIGIN, color=VIOLET).scale(1.5)
        labels = [
            ("Undo", LEFT*4 + UP*1.5),
            ("Browser\nHistory", RIGHT*4 + UP*1.5),
            ("Function\nCalls", LEFT*4 + DOWN*1.6),
            ("Recursion", RIGHT*4 + DOWN*1.6),
        ]
        self.play(FadeIn(center), run_time=0.5)
        for text, pos in labels:
            box = RoundedRectangle(width=2.5, height=1.0, corner_radius=0.15, stroke_color=CYAN, fill_color=PANEL, fill_opacity=0.92)
            txt = Text(text, color=CREAM, font_size=26).move_to(box.get_center())
            g = VGroup(box, txt).move_to(pos)
            arr = Arrow(center.get_center(), g.get_center(), color=CYAN, buff=0.35, stroke_width=4)
            self.play(GrowArrow(arr), FadeIn(g, scale=0.95), run_time=0.55)
        cap = bottom_caption("Stacks appear whenever the latest action must be handled first.")
        self.play(FadeIn(cap, shift=UP), run_time=0.6)
        self.wait(1.4)


class StackScene07Summary(StackBase):
    def construct(self):
        self.setup_scene("Stack Summary", "Three ideas to remember")
        bullets = VGroup(
            Text("1. Stack follows LIFO", color=CREAM, font_size=34),
            Text("2. Push adds to the top", color=CREAM, font_size=34),
            Text("3. Pop removes from the top", color=CREAM, font_size=34),
            Text("4. Peek reads the top", color=CREAM, font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).shift(LEFT*2.7)
        frame = make_stack_frame().scale(0.75).shift(RIGHT*3.2 + DOWN*0.3)
        items = VGroup(stack_item(10, -1.25, width=2.0), stack_item(20, -0.78, width=2.0), stack_item(30, -0.31, width=2.0)).scale(0.75).shift(RIGHT*3.2 + DOWN*0.3)
        self.play(FadeIn(bullets, shift=RIGHT), Create(frame), FadeIn(items), run_time=1.2)
        self.play(Indicate(bullets[0], color=VIOLET), Indicate(items[-1], color=YELLOW), run_time=1.1)
        cap = bottom_caption("A stack is simple, but extremely useful in programming.")
        self.play(FadeIn(cap, shift=UP), run_time=0.6)
        self.wait(1.5)
