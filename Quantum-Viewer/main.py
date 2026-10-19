
    
  
"""
GENESIS — Quantum State Visualizer
A small interactive 3D Bloch-sphere visualizer for a single qubit.

Run with:
    python genesis.py

The visualization opens in your default web browser.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ---------------------------------------------------------------------------
# Quantum state utilities
# ---------------------------------------------------------------------------

def qubit_state(theta: float, phi: float) -> np.ndarray:
    """Return the normalized state vector for a pure qubit on the Bloch sphere."""
    alpha = np.cos(theta / 2.0)
    beta = np.exp(1j * phi) * np.sin(theta / 2.0)
    return np.array([alpha, beta], dtype=complex)


def measurement_probabilities(state: np.ndarray) -> tuple[float, float]:
    """Calculate the probabilities of measuring |0> and |1>."""
    p0 = float(np.abs(state[0]) ** 2)
    p1 = float(np.abs(state[1]) ** 2)
    return p0, p1


def bloch_vector(state: np.ndarray) -> np.ndarray:
    """Convert a normalized pure-qubit state into its Bloch-sphere vector."""
    alpha, beta = state
    x = 2.0 * np.real(np.conj(alpha) * beta)
    y = 2.0 * np.imag(np.conj(alpha) * beta)
    z = float(np.abs(alpha) ** 2 - np.abs(beta) ** 2)
    return np.array([x, y, z], dtype=float)


# ---------------------------------------------------------------------------
# Visualization helpers
# ---------------------------------------------------------------------------

def add_bloch_sphere(fig: go.Figure) -> None:
    """Add a wireframe Bloch sphere, coordinate axes, and basis labels."""
    u = np.linspace(0, 2 * np.pi, 48)
    v = np.linspace(0, np.pi, 32)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones_like(u), np.cos(v))

    # Draw the sphere as a subtle wireframe.
    fig.add_trace(go.Surface(
        x=x, y=y, z=z,
        surfacecolor=np.zeros_like(z),
        colorscale=[[0, "#242039"], [1, "#242039"]],
        opacity=0.16,
        showscale=False,
        hoverinfo="skip",
        name="Bloch sphere",
        contours={
            "x": {"show": True, "color": "#51476d", "width": 1},
            "y": {"show": True, "color": "#51476d", "width": 1},
            "z": {"show": True, "color": "#51476d", "width": 1},
        },
    ))

    # Coordinate axes through the center of the sphere.
    axis_color = "#716a88"
    for axis, end in [
        ("X", (1.25, 0, 0)),
        ("Y", (0, 1.25, 0)),
        ("Z", (0, 0, 1.25)),
    ]:
        fig.add_trace(go.Scatter3d(
            x=[-end[0], end[0]],
            y=[-end[1], end[1]],
            z=[-end[2], end[2]],
            mode="lines",
            line=dict(color=axis_color, width=3),
            hoverinfo="skip",
            showlegend=False,
        ))
        fig.add_trace(go.Scatter3d(
            x=[end[0] * 1.08],
            y=[end[1] * 1.08],
            z=[end[2] * 1.08],
            mode="text",
            text=[axis],
            textfont=dict(color="#d9d3ed", size=13),
            hoverinfo="skip",
            showlegend=False,
        ))

