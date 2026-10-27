"""Quanta-Core — High-Performance Quantum Computing & Statevector Simulation Engine."""

from .state import QuantumState
from .circuit import QuantumCircuit
from .density import DensityMatrix
from . import gates
from .algorithms import create_bell_state, run_quantum_teleportation, grovers_algorithm
from .visualizer import render_bloch_ascii, render_histogram

__version__ = "0.1.0"
__all__ = [
    "QuantumState",
    "QuantumCircuit",
    "DensityMatrix",
    "gates",
    "create_bell_state",
    "run_quantum_teleportation",
    "grovers_algorithm",
    "render_bloch_ascii",
    "render_histogram"
]
