"""Builds ../../animation.css: the hand-written rules in static.css, then the generated
keyframes. One 14 s timeline; every animation shares it, so the scene and the steps stay
in step. Edit the timing here (times are in seconds), then run:

    python3 tools/animation/build.py
"""
import os
import math, random

D = 14.0
def pct(t): return round(t / D * 100, 3)

EASE = "cubic-bezier(.4,0,.2,1)"      # general
SOFT = "cubic-bezier(.45,0,.55,1)"     # voice
OUT  = "cubic-bezier(.16,1,.3,1)"      # quick settle

def kf(name, stops):
    """stops: [(t, 'css declarations', easing-for-the-interval-after or None)]"""
    # Without an explicit 0% and 100% the browser fills the gap from the element's own
    # style, which is what made the lines flash to the mark at the end of the loop.
    assert stops[0][0] == 0 and stops[-1][0] == 14, f"{name} must start at 0 and end at 14 s"
    out = [f"@keyframes {name} {{"]
    for t, decl, ease in stops:
        e = f" animation-timing-function: {ease};" if ease else ""
        decl = decl.strip().rstrip(";") + ";"
        out.append(f"  {pct(t)}% {{ {decl}{e} }}")
    out.append("}")
    return "\n".join(out)

css = []

# ---- keys: pressed one after another, lifted together
KEY_UP   = "transform: translateY(0); box-shadow: 0 .22em 0 var(--key-edge); background-color: var(--key-face); border-color: var(--key-edge);"
KEY_DOWN = "transform: translateY(.2em); box-shadow: 0 .02em 0 var(--key-edge-down); background-color: var(--key-down); border-color: var(--key-edge-down);"
for n, t0 in ((1, 1.00), (2, 1.25), (3, 1.50)):
    css.append(kf(f"key{n}", [
        (0, KEY_UP, None), (t0, KEY_UP, OUT), (t0 + .16, KEY_DOWN, None),
        (8.20, KEY_DOWN, OUT), (8.45, KEY_UP, None), (14, KEY_UP, None)]))

# ---- menu bar glyph: the app's real states
css.append(kf("glyph-ready", [
    (0, "opacity:1", None), (1.70, "opacity:1", EASE), (1.88, "opacity:0", None),
    (8.95, "opacity:0", EASE), (9.12, "opacity:1", None), (14, "opacity:1", None)]))
css.append(kf("glyph-listen", [
    (0, "opacity:0", None), (1.70, "opacity:0", EASE), (1.88, "opacity:1", None),
    (8.20, "opacity:1", EASE), (8.36, "opacity:0", None), (14, "opacity:0", None)]))
css.append(kf("glyph-trans", [
    (0, "opacity:0", None), (8.20, "opacity:0", EASE), (8.36, "opacity:1", None),
    (8.95, "opacity:1", EASE), (9.12, "opacity:0", None), (14, "opacity:0", None)]))

# ---- the soft sound, drawn as two rings leaving the menu bar icon
def ring(name, t0, dur, peak, grow):
    css.append(kf(name, [
        (0, "opacity:0; transform: scale(1)", None), (t0, "opacity:0; transform: scale(1)", OUT),
        (t0 + .05, f"opacity:{peak}; transform: scale(1.1)", "cubic-bezier(.2,.6,.3,1)"),
        (t0 + dur, f"opacity:0; transform: scale({grow})", None), (14, "opacity:0; transform: scale(1)", None)]))
ring("ring1", 9.00, 1.15, .65, 5.2)
ring("ring2", 9.14, 1.30, .40, 8.6)

# ---- voice: the Swell's five lines
# s = how much of the full mark's height each line shows; 1 is the finished mark.
rng = random.Random(11)
STEP = 0.12
phrases = [(2.95, 5.35), (5.85, 8.05)]
n_steps = int((8.05 - 2.85) / STEP) + 2
syl = []
for k in range(n_steps):
    t = 2.85 + k * STEP
    inside = any(a <= t <= b for a, b in phrases)
    if not inside:
        syl.append(0.10)
        continue
    base = rng.uniform(.42, 1.0)
    syl.append(base)
# word gaps: a dip every few syllables
for k in range(n_steps):
    if k % 6 == 5 and syl[k] > .2:
        syl[k] *= .35
smooth = [(syl[max(k-1,0)] * .25 + syl[k] * .5 + syl[min(k+1,n_steps-1)] * .25) for k in range(n_steps)]

def voice_value(i, k):
    kk = k - round(i * 0.07 / STEP * 1)          # each line trails the one outside it
    kk = max(0, min(n_steps - 1, kk))
    base = smooth[kk]
    wobble = 1 + .07 * math.sin(2 * math.pi * (kk * STEP * (1.7 + .37 * i)) + i)
    return max(.05, min(1.08, base * 1.02 * wobble))

IDLE = "transform: scaleY(.02); opacity:.5"
for i in range(5):
    stops = [(0, IDLE, None), (1.70, IDLE, SOFT)]
    # listening: a slow breath while waiting for a voice
    stops.append((2.35, "transform: scaleY(.13); opacity:.8", SOFT))
    stops.append((2.85, "transform: scaleY(.09); opacity:.85", SOFT))
    for k in range(n_steps):
        t = 2.85 + k * STEP + .12
        if t > 8.05: break
        v = voice_value(i, k)
        stops.append((t, f"transform: scaleY({v:.3f}); opacity:1", SOFT))
    # release: drop flat, wait for the text, then swell once into the finished mark
    stops.append((8.20, "transform: scaleY(.10); opacity:1", OUT))
    stops.append((8.50, "transform: scaleY(.02); opacity:.7", EASE))
    stops.append((9.00 + i * .05, "transform: scaleY(.02); opacity:.8", "cubic-bezier(.3,1.5,.5,1)"))
    stops.append((9.75 + i * .05, "transform: scaleY(1); opacity:1", EASE))
    stops.append((13.00, "transform: scaleY(1); opacity:1", SOFT))
    stops.append((13.95, IDLE, None))
    stops.append((14, IDLE, None))
    css.append(kf(f"voice{i+1}", stops))

# ---- clipboard: the text arrives after the ping
css.append(kf("text-in", [
    (0, "clip-path: inset(0 100% 0 0); opacity:1", None), (9.10, "clip-path: inset(0 100% 0 0); opacity:1", "cubic-bezier(.3,.7,.2,1)"),
    (9.95, "clip-path: inset(0 0 0 0); opacity:1", None), (13.00, "clip-path: inset(0 0 0 0); opacity:1", EASE),
    (13.60, "clip-path: inset(0 0 0 0); opacity:0", None), (13.62, "clip-path: inset(0 100% 0 0); opacity:0", None),
    (14, "clip-path: inset(0 100% 0 0); opacity:1", None)]))
css.append(kf("pill", [
    (0, "stroke-opacity:.28", None), (9.00, "stroke-opacity:.28", EASE), (9.25, "stroke-opacity:.9", EASE),
    (10.2, "stroke-opacity:.5", None), (13.00, "stroke-opacity:.5", EASE), (13.8, "stroke-opacity:.28", None), (14, "stroke-opacity:.28", None)]))
css.append(kf("pill-icon", [
    (0, "opacity:.35", None), (9.00, "opacity:.35", EASE), (9.30, "opacity:1", EASE),
    (10.2, "opacity:.75", None), (13.00, "opacity:.75", EASE), (13.8, "opacity:.35", None), (14, "opacity:.35", None)]))

# ---- the three steps light up in turn
def step(name, a, b):
    DIM, LIT = "opacity:.36", "opacity:1"
    stops = [(0, DIM, None)]
    if a > 0:
        stops += [(a - .05, DIM, EASE), (a + .30, LIT, None)]
    else:
        stops = [(0, LIT, None)]
    stops += [(b, LIT, EASE), (b + .35, DIM, None)]
    stops.append((14, DIM, None))
    css.append(kf(name, stops))
step("step-hold", 0.90, 2.95)
step("step-speak", 2.85, 8.15)
step("step-release", 8.15, 13.00)

here = os.path.dirname(os.path.abspath(__file__))
static = open(os.path.join(here, "static.css")).read()
out = os.path.join(here, "..", "..", "animation.css")
with open(out, "w") as f:
    f.write(static + "\n".join(css) + "\n")
print("wrote", os.path.normpath(out))
