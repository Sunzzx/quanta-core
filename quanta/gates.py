"""Universal Quantum Gates and Unitary Matrix Algebra.

Supports single-qubit, controlled two-qubit, and multi-qubit Toffoli gates.
"""

import numpy as np
from typing import List, Tuple

# Identity
I2 = np.eye(2, dtype=np.complex128)

# Pauli Gates
X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)

# Hadamard
H = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=np.complex128)

# Phase (S) and T gates
S = np.array([[1, 0], [0, 1j]], dtype=np.complex128)
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=np.complex128)

def RX(theta: float) -> np.ndarray:
    """Rotation around X axis: exp(-i theta X / 2)."""
    return np.array([
        [np.cos(theta / 2), -1j * np.sin(theta / 2)],
        [-1j * np.sin(theta / 2), np.cos(theta / 2)]
    ], dtype=np.complex128)

def RY(theta: float) -> np.ndarray:
    """Rotation around Y axis: exp(-i theta Y / 2)."""
    return np.array([
        [np.cos(theta / 2), -np.sin(theta / 2)],
        [np.sin(theta / 2), np.cos(theta / 2)]
    ], dtype=np.complex128)

def RZ(theta: float) -> np.ndarray:
    """Rotation around Z axis: exp(-i theta Z / 2)."""
    return np.array([
        [np.exp(-1j * theta / 2), 0],
        [0, np.exp(1j * theta / 2)]
    ], dtype=np.complex128)

def lift_single_qubit_gate(num_qubits: int, target_qubit: int, gate_2x2: np.ndarray) -> np.ndarray:
    """Embed a 2x2 gate on a target qubit into full 2^n space via Kronecker tensor product."""
    op = np.array([[1.0]], dtype=np.complex128)
    for q in range(num_qubits):
        if q == target_qubit:
            op = np.kron(op, gate_2x2)
        else:
            op = np.kron(op, I2)
    return op

def build_cnot(num_qubits: int, control: int, target: int) -> np.ndarray:
    """Construct a full 2^n x 2^n Controlled-NOT unitary matrix."""
    dim = 2 ** num_qubits
    U = np.zeros((dim, dim), dtype=np.complex128)
    shift_ctrl = num_qubits - 1 - control
    shift_tgt = num_qubits - 1 - target

    for idx in range(dim):
        is_ctrl_set = (idx >> shift_ctrl) & 1
        if is_ctrl_set:
            # Flip target bit
            out_idx = idx ^ (1 << shift_tgt)
        else:
            out_idx = idx
        U[out_idx, idx] = 1.0
    return U

def build_cz(num_qubits: int, control: int, target: int) -> np.ndarray:
    """Construct a full 2^n x 2^n Controlled-Z unitary matrix."""
    dim = 2 ** num_qubits
    U = np.zeros((dim, dim), dtype=np.complex128)
    shift_ctrl = num_qubits - 1 - control
    shift_tgt = num_qubits - 1 - target

    for idx in range(dim):
        is_ctrl_set = (idx >> shift_ctrl) & 1
        is_tgt_set = (idx >> shift_tgt) & 1
        phase = -1.0 if (is_ctrl_set and is_tgt_set) else 1.0
        U[idx, idx] = phase
    return U

def build_toffoli(num_qubits: int, ctrl1: int, ctrl2: int, target: int) -> np.ndarray:
    """Construct a 3-qubit Controlled-Controlled-NOT (Toffoli) gate."""
    dim = 2 ** num_qubits
    U = np.zeros((dim, dim), dtype=np.complex128)
    s_c1 = num_qubits - 1 - ctrl1
    s_c2 = num_qubits - 1 - ctrl2
    s_t = num_qubits - 1 - target

    for idx in range(dim):
        c1 = (idx >> s_c1) & 1
        c2 = (idx >> s_c2) & 1
        if c1 and c2:
            out_idx = idx ^ (1 << s_t)
        else:
            out_idx = idx
        U[out_idx, idx] = 1.0
    return U

def build_swap(num_qubits: int, q1: int, q2: int) -> np.ndarray:
    """Construct a 2-qubit SWAP gate."""
    dim = 2 ** num_qubits
    U = np.zeros((dim, dim), dtype=np.complex128)
    s1 = num_qubits - 1 - q1
    s2 = num_qubits - 1 - q2

    for idx in range(dim):
        b1 = (idx >> s1) & 1
        b2 = (idx >> s2) & 1
        if b1 != b2:
            # swap bits
            out_idx = idx ^ ((1 << s1) | (1 << s2))
        else:
            out_idx = idx
        U[out_idx, idx] = 1.0
    return U
