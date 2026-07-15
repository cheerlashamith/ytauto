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

# ─── NEW: Binary Tree / BST ─────────────────────────────────────────────────

def _make_node(val, node_color=CYAN, radius=0.42):
    c = Circle(radius=radius, stroke_color=node_color, stroke_width=5,
               fill_color="#0d1117", fill_opacity=0.96)
    t = Text(str(val), font_size=24, color=WHITE, weight=BOLD).move_to(c.get_center())
    return VGroup(c, t)

def tree(scene, vd):
    """Animated binary tree. Supports BST, general trees, heaps."""
    # Parse nodes from visual_data
    raw_nodes = vd.get('nodes') or vd.get('values') or [50, 30, 70, 20, 40, 60, 80]
    highlight_val = vd.get('highlight') or vd.get('search')
    insert_val = vd.get('insert')
    tree_type = str(vd.get('tree_type', 'bst')).lower()

    # Build BST structure from node list
    try:
        vals = [int(str(n).strip()) if isinstance(n, (int, float, str)) and str(n).strip().lstrip('-').isdigit() else 0 for n in raw_nodes[:15]]
    except Exception:
        vals = [50, 30, 70, 20, 40, 60, 80]
    vals = vals or [50, 30, 70, 20, 40, 60, 80]

    # BST insertion to determine structure
    class BSTNode:
        def __init__(self, v): self.v=v; self.left=None; self.right=None
    def bst_insert(root, v):
        if root is None: return BSTNode(v)
        if v < root.v: root.left = bst_insert(root.left, v)
        else: root.right = bst_insert(root.right, v)
        return root

    root = None
    if tree_type == 'bst':
        for v in vals:
            root = bst_insert(root, v)
    else:
        # Just use array order as level-order tree
        nodes_arr = [BSTNode(v) for v in vals]
        for i, n in enumerate(nodes_arr):
            if 2*i+1 < len(nodes_arr): n.left = nodes_arr[2*i+1]
            if 2*i+2 < len(nodes_arr): n.right = nodes_arr[2*i+2]
        root = nodes_arr[0] if nodes_arr else None

    if root is None:
        return

    # Assign positions via in-order traversal
    positions = {}
    counter = [0]
    depth_counts = {}

    def assign_x(node, depth=0):
        if node is None: return
        assign_x(node.left, depth+1)
        positions[id(node)] = (counter[0], depth)
        depth_counts[depth] = depth_counts.get(depth, 0) + 1
        counter[0] += 1
        assign_x(node.right, depth+1)

    assign_x(root)

    # Scale positions to screen coordinates
    max_x = max((p[0] for p in positions.values()), default=0)
    max_d = max((p[1] for p in positions.values()), default=0)
    x_scale = min(10.0 / max(max_x, 1), 1.5)
    y_scale = 1.4

    def screen_pos(node):
        x_idx, depth = positions[id(node)]
        cx = (x_idx - max_x/2) * x_scale
        cy = 1.8 - depth * y_scale
        return np.array([cx, cy, 0])

    # Build Manim objects
    node_mobs = {}
    edge_mobs = []

    def build_mobs(node):
        if node is None: return
        ncolor = YELLOW if (highlight_val is not None and node.v == highlight_val) else (
                 GREEN if (insert_val is not None and node.v == insert_val) else CYAN)
        m = _make_node(node.v, ncolor).move_to(screen_pos(node))
        node_mobs[id(node)] = m
        for child in [node.left, node.right]:
            if child:
                build_mobs(child)
                # Edge from parent to child
                edge_mobs.append((id(node), id(child)))

    build_mobs(root)

    # Animate root first, then BFS layer by layer
    from collections import deque
    queue = deque([root])
    layers = [[root]]
    visited = {id(root)}
    def get_children(n):
        ch = []
        if n.left and id(n.left) not in visited: ch.append(n.left); visited.add(id(n.left))
        if n.right and id(n.right) not in visited: ch.append(n.right); visited.add(id(n.right))
        return ch

    all_layers = []
    current_layer = [root]
    while current_layer:
        all_layers.append(current_layer)
        next_layer = []
        for n in current_layer:
            next_layer.extend(get_children(n))
        current_layer = next_layer

    # Draw root
    scene.play(FadeIn(node_mobs[id(root)], scale=0.7), run_time=0.5)

    # Draw layer by layer with edges
    for layer_idx, layer in enumerate(all_layers[1:], 1):
        anims = []
        for node in layer:
            anims.append(FadeIn(node_mobs[id(node)], scale=0.7))
            # Draw edge from parent
            parent_id = None
            for eid, cid in edge_mobs:
                if cid == id(node): parent_id = eid; break
            if parent_id:
                p_mob = node_mobs[parent_id]
                c_mob = node_mobs[id(node)]
                edge = Line(p_mob.get_center(), c_mob.get_center(),
                           color=CYAN, stroke_width=3, stroke_opacity=0.8)
                edge.set_z_index(-1)
                anims.append(Create(edge))
        if anims:
            scene.play(*anims, run_time=0.45)

    # Highlight search path if specified
    if highlight_val is not None:
        def find_path(node, target, path=[]):
            if node is None: return None
            path = path + [node]
            if node.v == target: return path
            if target < node.v: return find_path(node.left, target, path)
            return find_path(node.right, target, path)
        path = find_path(root, highlight_val)
        if path:
            for pnode in path:
                scene.play(Indicate(node_mobs[id(pnode)], color=YELLOW, scale_factor=1.3), run_time=0.4)

    # Insert animation
    if insert_val is not None:
        ins_label = txt(f"Insert: {insert_val}", 30, GREEN).to_corner(UR, buff=0.5)
        scene.play(FadeIn(ins_label), run_time=0.4)


# ─── NEW: Linked List ────────────────────────────────────────────────────────

def linked_list(scene, vd):
    """Animated singly or doubly linked list."""
    vals = vd.get('values') or vd.get('nodes') or ['head', 'A', 'B', 'C', 'null']
    highlight = vd.get('highlight')
    doubly = vd.get('doubly', False)
    vals = [str(v) for v in vals[:8]]

    nodes = []
    for i, v in enumerate(vals):
        is_null = str(v).lower() in ('null', 'none', '∅', 'nil')
        node_color = YELLOW if v == highlight else (GRAY if is_null else CYAN)
        box = rounded_box(v, width=1.4, height=0.65, color=node_color)
        nodes.append((box, is_null))

    group = VGroup(*[n for n, _ in nodes]).arrange(RIGHT, buff=0.55).move_to(ORIGIN)

    for i, (mob, is_null) in enumerate(nodes):
        scene.play(FadeIn(mob, scale=0.8), run_time=0.3)
        if i < len(nodes) - 1:
            start = mob.get_right()
            end = nodes[i+1][0].get_left()
            if doubly:
                arr1 = Arrow(start, end, buff=0.08, color=CYAN, stroke_width=4)
                arr2 = Arrow(end + DOWN*0.15, start + DOWN*0.15, buff=0.08, color=ORANGE, stroke_width=3)
                scene.play(GrowArrow(arr1), GrowArrow(arr2), run_time=0.3)
            else:
                arr = Arrow(start, end, buff=0.08, color=CYAN, stroke_width=4)
                scene.play(GrowArrow(arr), run_time=0.3)

    if highlight:
        for i, (mob, _) in enumerate(nodes):
            if str(vals[i]) == str(highlight):
                scene.play(Indicate(mob, color=YELLOW, scale_factor=1.25), run_time=0.5)


# ─── NEW: Stack ──────────────────────────────────────────────────────────────

def stack(scene, vd):
    """Animated stack (LIFO) with push/pop."""
    vals = vd.get('values') or vd.get('items') or ['Base', 'Data', 'Top']
    ops = vd.get('operations') or []  # list of {'op':'push','val':'X'} or {'op':'pop'}
    vals = [str(v) for v in vals[:6]]

    stack_mobs = []
    base_y = -1.8
    box_h = 0.7
    box_w = 2.2

    # Draw label
    scene.play(FadeIn(txt("STACK (LIFO)", 28, VIOLET, BOLD).to_edge(UP, buff=1.1)), run_time=0.35)
    # Draw stack outline
    outline = Rectangle(width=box_w+0.15, height=len(vals)*box_h+0.2,
                        stroke_color=CYAN, stroke_width=3, fill_opacity=0)
    outline.move_to([0, base_y + len(vals)*box_h/2, 0])
    scene.play(Create(outline), run_time=0.4)

    for i, v in enumerate(vals):
        y_pos = base_y + i * box_h + box_h/2
        box = rounded_box(v, box_w, box_h-0.08,
                         color=YELLOW if i == len(vals)-1 else CYAN)
        box.move_to([0, y_pos, 0])
        stack_mobs.append(box)
        scene.play(FadeIn(box, shift=UP*0.2), run_time=0.3)

    # Top pointer
    if stack_mobs:
        top_arrow = Arrow(RIGHT*2.2, RIGHT*1.3+UP*0*(box_h), color=YELLOW, stroke_width=4)
        top_arrow.next_to(stack_mobs[-1], RIGHT, buff=0.1)
        top_label = txt("TOP", 22, YELLOW).next_to(top_arrow, RIGHT, buff=0.1)
        scene.play(GrowArrow(top_arrow), FadeIn(top_label), run_time=0.4)


# ─── NEW: Sorting Bars ───────────────────────────────────────────────────────

def sorting(scene, vd):
    """Visualise a sorting pass with highlighted comparisons."""
    vals = vd.get('values') or vd.get('array') or [64, 34, 25, 12, 22, 11, 90]
    swap_pairs = vd.get('swaps') or []
    highlight_idx = vd.get('highlight') or []
    vals = [int(v) for v in vals[:12] if str(v).isdigit() or (str(v).lstrip('-').isdigit())]
    if not vals: vals = [64, 34, 25, 12, 22, 11, 90]

    max_v = max(vals) if vals else 1
    bar_w = min(0.9, 10.0 / len(vals) - 0.1)
    total_w = (bar_w + 0.1) * len(vals)
    start_x = -total_w / 2 + bar_w / 2

    bars = []
    labels = []
    for i, v in enumerate(vals):
        h = 3.5 * v / max_v
        bcolor = YELLOW if i in highlight_idx else CYAN
        bar = Rectangle(width=bar_w, height=h,
                       stroke_color=bcolor, stroke_width=3,
                       fill_color=bcolor, fill_opacity=0.6)
        bar.move_to([start_x + i*(bar_w+0.1), -1.5 + h/2, 0])
        lab = txt(str(v), 18).next_to(bar, DOWN, buff=0.1)
        bars.append(bar); labels.append(lab)

    scene.play(*[FadeIn(b, shift=UP*0.3) for b in bars],
               *[FadeIn(l) for l in labels], run_time=0.6)

    # Animate swaps
    for pair in swap_pairs[:3]:
        if len(pair) == 2:
            i, j = int(pair[0]), int(pair[1])
            if 0 <= i < len(bars) and 0 <= j < len(bars):
                scene.play(bars[i].animate.set_color(RED),
                          bars[j].animate.set_color(RED), run_time=0.25)
                # Swap positions
                pi, pj = bars[i].get_center().copy(), bars[j].get_center().copy()
                scene.play(bars[i].animate.move_to(pj),
                          bars[j].animate.move_to(pi), run_time=0.4)
                bars[i].set_color(CYAN); bars[j].set_color(CYAN)
                bars[i], bars[j] = bars[j], bars[i]


# ─── NEW: Hash Table ─────────────────────────────────────────────────────────

def hash_table(scene, vd):
    """Show a hash table with buckets and key-value pairs."""
    size = int(vd.get('size', 7))
    pairs = vd.get('pairs') or vd.get('entries') or [('key1', 'v1'), ('key2', 'v2')]
    size = min(size, 10)

    bucket_h = 0.6; bucket_w = 2.8; start_y = 2.0
    buckets = []
    for i in range(size):
        y = start_y - i*bucket_h
        idx_box = rounded_box(str(i), 0.6, bucket_h-0.06, color=VIOLET)
        idx_box.move_to([-3.5, y, 0])
        val_box = rounded_box('', bucket_w, bucket_h-0.06, color=GRAY)
        val_box.move_to([-3.5+0.3+bucket_w/2+0.35, y, 0])
        buckets.append((i, idx_box, val_box))

    all_mobs = [m for _, ib, vb in buckets for m in [ib, vb]]
    scene.play(*[FadeIn(m, run_time=0.03) for m in all_mobs], run_time=0.5)

    for key, val in pairs[:size]:
        bucket_idx = hash(str(key)) % size
        _, ib, vb = buckets[bucket_idx]
        label_mob = txt(f"{key}→{val}", 20, GREEN).move_to(vb.get_center())
        scene.play(Indicate(ib, color=YELLOW), FadeIn(label_mob), run_time=0.4)

