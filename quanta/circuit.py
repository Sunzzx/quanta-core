"""Quantum Circuit Engine and Execution Graph.

Provides an intuitive circuit composition API with automatic unitary compilation
and ASCII circuit visualization.
"""

from __future__ import annotations
from typing import List, Tuple, Any, Dict, Optional
import numpy as np
from .state import QuantumState
from . import gates

class GateOperation:
    def __init__(self, name: str, qubits: List[int], params: Optional[Dict[str, float]] = None):
        self.name = name
        self.qubits = qubits
        self.params = params or {}

    def __repr__(self) -> str:
        param_str = f"({self.params})" if self.params else ""
        return f"{self.name}{param_str}[{', '.join(map(str, self.qubits))}]"


class QuantumCircuit:
    """Represents a quantum circuit acting on n qubits."""

    def __init__(self, num_qubits: int):
        self.num_qubits = num_qubits
        self.ops: List[GateOperation] = []

    def h(self, qubit: int) -> QuantumCircuit:
        self.ops.append(GateOperation("H", [qubit]))
        return self

    def x(self, qubit: int) -> QuantumCircuit:
        self.ops.append(GateOperation("X", [qubit]))
        return self

    def y(self, qubit: int) -> QuantumCircuit:
        self.ops.append(GateOperation("Y", [qubit]))
        return self

    def z(self, qubit: int) -> QuantumCircuit:
        self.ops.append(GateOperation("Z", [qubit]))
        return self

    def s(self, qubit: int) -> QuantumCircuit:
        self.ops.append(GateOperation("S", [qubit]))
        return self

    def t(self, qubit: int) -> QuantumCircuit:
        self.ops.append(GateOperation("T", [qubit]))
        return self

    def rx(self, qubit: int, theta: float) -> QuantumCircuit:
        self.ops.append(GateOperation("RX", [qubit], {"theta": theta}))
        return self

    def ry(self, qubit: int, theta: float) -> QuantumCircuit:
        self.ops.append(GateOperation("RY", [qubit], {"theta": theta}))
        return self

    def rz(self, qubit: int, theta: float) -> QuantumCircuit:
        self.ops.append(GateOperation("RZ", [qubit], {"theta": theta}))
        return self

    def cx(self, control: int, target: int) -> QuantumCircuit:
        self.ops.append(GateOperation("CX", [control, target]))
        return self

    def cz(self, control: int, target: int) -> QuantumCircuit:
        self.ops.append(GateOperation("CZ", [control, target]))
        return self

    def swap(self, q1: int, q2: int) -> QuantumCircuit:
        self.ops.append(GateOperation("SWAP", [q1, q2]))
        return self

    def toffoli(self, ctrl1: int, ctrl2: int, target: int) -> QuantumCircuit:
        self.ops.append(GateOperation("CCX", [ctrl1, ctrl2, target]))
        return self

    def execute(self, initial_state: Optional[QuantumState] = None) -> QuantumState:
        """Execute circuit operations on the statevector."""
        if initial_state is None:
            state = QuantumState(self.num_qubits)
        else:
            state = QuantumState(self.num_qubits, initial_state.vec.copy())

        for op in self.ops:
            if op.name == "H":
                U = gates.lift_single_qubit_gate(self.num_qubits, op.qubits[0], gates.H)
            elif op.name == "X":
                U = gates.lift_single_qubit_gate(self.num_qubits, op.qubits[0], gates.X)
            elif op.name == "Y":
                U = gates.lift_single_qubit_gate(self.num_qubits, op.qubits[0], gates.Y)
            elif op.name == "Z":
                U = gates.lift_single_qubit_gate(self.num_qubits, op.qubits[0], gates.Z)
            elif op.name == "S":
                U = gates.lift_single_qubit_gate(self.num_qubits, op.qubits[0], gates.S)
            elif op.name == "T":
                U = gates.lift_single_qubit_gate(self.num_qubits, op.qubits[0], gates.T)
            elif op.name == "RX":
                U = gates.lift_single_qubit_gate(self.num_qubits, op.qubits[0], gates.RX(op.params["theta"]))
            elif op.name == "RY":
                U = gates.lift_single_qubit_gate(self.num_qubits, op.qubits[0], gates.RY(op.params["theta"]))
            elif op.name == "RZ":
                U = gates.lift_single_qubit_gate(self.num_qubits, op.qubits[0], gates.RZ(op.params["theta"]))
            elif op.name == "CX":
                U = gates.build_cnot(self.num_qubits, op.qubits[0], op.qubits[1])
            elif op.name == "CZ":
                U = gates.build_cz(self.num_qubits, op.qubits[0], op.qubits[1])
            elif op.name == "SWAP":
                U = gates.build_swap(self.num_qubits, op.qubits[0], op.qubits[1])
            elif op.name == "CCX":
                U = gates.build_toffoli(self.num_qubits, op.qubits[0], op.qubits[1], op.qubits[2])
            else:
                raise ValueError(f"Unsupported gate operation: {op.name}")

            state.vec = U @ state.vec

        return state

    def draw(self) -> str:
        """Generate a clean ASCII diagram of the quantum circuit."""
        lines = [f"q{q}: |0> ──" for q in range(self.num_qubits)]

        for op in self.ops:
            if len(op.qubits) == 1:
                q = op.qubits[0]
                gate_str = f"[{op.name}]──"
                lines[q] += gate_str
                # Pad others
                pad = len(gate_str)
                for other in range(self.num_qubits):
                    if other != q:
                        lines[other] += "─" * pad
            elif len(op.qubits) == 2 and op.name == "CX":
                c, t = op.qubits[0], op.qubits[1]
                ctrl_str = "──●──"
                tgt_str = "──⊕──"
                lines[c] += ctrl_str
                lines[t] += tgt_str
                for other in range(self.num_qubits):
                    if other not in (c, t):
                        lines[other] += "─────"
            else:
                for q in range(self.num_qubits):
                    if q in op.qubits:
                        lines[q] += f"[{op.name}]──"
                    else:
                        lines[q] += "──────"

        return chr(10).join(lines)
