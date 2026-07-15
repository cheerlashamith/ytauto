from manim import *
BG = "#0A0F1E"
PANEL = "#0B1833"
CREAM = "#DEDBC8"
WHITE = "#FFFFFF"
MUTED = "#B0BEC5"
CYAN = "#00E5FF"
BLUE = "#00A8FF"
YELLOW = "#FFD600"
ORANGE = "#FF6F00"
GREEN = "#00E676"
RED = "#FF1744"
VIOLET = "#A98BFF"
COLOR_MAP = {"accent_electric_blue":CYAN,"accent_electric_yellow":YELLOW,"accent_warm_orange":ORANGE,"accent_soft_green":GREEN,"accent_warm_red":RED,"text_primary":WHITE,"text_secondary":MUTED}
def resolve_color(value, default=CYAN):
    return COLOR_MAP.get(str(value), str(value) if value else default)
