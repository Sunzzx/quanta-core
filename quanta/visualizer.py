"""Bloch Sphere Visualizer & Statevector Terminal Display.

Renders Bloch sphere coordinates (theta, phi) and ASCII bar distributions.
"""

import math
from typing import Dict, Tuple

def render_bloch_ascii(x: float, y: float, z: float) -> str:
    """ASCII visual representation of the Bloch vector on the unit sphere."""
    # Spherical coordinates
    r = math.sqrt(x*x + y*y + z*z)
    theta = math.acos(max(-1.0, min(1.0, z / (r if r > 1e-9 else 1.0))))
    phi = math.atan2(y, x)

    art = f"""
        +Z |0>
          |     /
          |    /  (Bloch Vector)
          |   *  [r={r:.2f}, theta={math.degrees(theta):.1f}°, phi={math.degrees(phi):.1f}°]
          |  /
    ------o------ +Y
         /|
        / |
       /  |
     +X   | -Z |1>
    Coordinates: (x={x:+.3f}, y={y:+.3f}, z={z:+.3f})
"""
    return art

def render_histogram(counts: Dict[str, int], width: int = 40) -> str:
    """Render an ASCII histogram for classical measurement counts."""
    total = sum(counts.values()) if counts else 1
    lines = []
    for bitstring in sorted(counts.keys()):
        cnt = counts[bitstring]
        frac = cnt / total
        bar_len = int(round(frac * width))
        bar = "█" * bar_len
        lines.append(f"|{bitstring}>: {bar:<{width}} ({frac*100:5.1f}% | {cnt} shots)")
    return chr(10).join(lines)
