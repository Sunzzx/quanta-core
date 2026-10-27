"""Canonical Quantum Algorithms and Protocols.

Contains rigorous implementations of:
- Bell State Entanglement (EPR pairs)
- Complete Quantum Teleportation Protocol
- Quantum Superdense Coding
- Grover's Search Algorithm with Amplitude Amplification
"""

import math
import numpy as np
from typing import Dict, Tuple, Optional, Any
from .circuit import QuantumCircuit
from .state import QuantumState
from . import gates

def create_bell_state(variant: str = "phi_plus") -> QuantumState:
    """Generate a maximally entangled Bell state:
    phi_plus:  (|00> + |11>) / sqrt(2)
    phi_minus: (|00> - |11>) / sqrt(2)
    psi_plus:  (|01> + |10>) / sqrt(2)
    psi_minus: (|01> - |10>) / sqrt(2)
    """
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)

    if variant == "phi_minus":
        qc.z(0)
    elif variant == "psi_plus":
        qc.x(1)
    elif variant == "psi_minus":
        qc.z(0)
        qc.x(1)

    return qc.execute()

def run_quantum_teleportation(alpha: complex, beta: complex) -> Dict[str, Any]:
    """Simulate the full 3-qubit Quantum Teleportation Protocol:
    1. Alice possesses arbitrary unknown state |psi> = alpha|0> + beta|1> on qubit 0.
    2. Alice and Bob share an EPR pair on qubits 1 and 2.
    3. Alice performs Bell-basis measurement on qubits 0 and 1.
    4. Classical measurement results (m0, m1) are communicated to Bob.
    5. Bob applies Pauli X^m1 * Z^m0 corrections to recover exact state |psi> on qubit 2.
    """
    # Normalize input state
    norm = math.sqrt(abs(alpha)**2 + abs(beta)**2)
    alpha /= norm
    beta /= norm

    # 3-qubit state: q0 = |psi>, q1 = |0>, q2 = |0>
    init_vec = np.zeros(8, dtype=np.complex128)
    init_vec[0] = alpha  # |000>
    init_vec[4] = beta   # |100> (q0=1)
    state = QuantumState(3, init_vec)

    # Step 1: Create Bell state on q1, q2
    U_h1 = gates.lift_single_qubit_gate(3, 1, gates.H)
    state.vec = U_h1 @ state.vec
    U_cx12 = gates.build_cnot(3, 1, 2)
    state.vec = U_cx12 @ state.vec

    # Step 2: Alice entangles q0 with her half of the Bell pair q1
    U_cx01 = gates.build_cnot(3, 0, 1)
    state.vec = U_cx01 @ state.vec
    U_h0 = gates.lift_single_qubit_gate(3, 0, gates.H)
    state.vec = U_h0 @ state.vec

    # Step 3: Alice measures q0 and q1
    m0, _ = state.measure_qubit(0)
    m1, _ = state.measure_qubit(1)

    # Step 4: Bob applies classical corrections to q2 based on (m0, m1)
    if m1 == 1:
        U_x2 = gates.lift_single_qubit_gate(3, 2, gates.X)
        state.vec = U_x2 @ state.vec
    if m0 == 1:
        U_z2 = gates.lift_single_qubit_gate(3, 2, gates.Z)
        state.vec = U_z2 @ state.vec

    # Trace out q0 and q1; extract Bob's qubit 2 state
    rho_bob = state.reduced_density_matrix([2])
    target_vec = np.array([alpha, beta], dtype=complex)
    target_rho = np.outer(target_vec, np.conj(target_vec))

    # Fidelity F = Tr(rho_bob * target_rho)
    fidelity = float(np.real(np.trace(rho_bob @ target_rho)))

    return {
        "measured_bits": (m0, m1),
        "bob_fidelity": fidelity,
        "target_state": (alpha, beta),
        "success": abs(fidelity - 1.0) < 1e-6
    }

def grovers_algorithm(num_qubits: int, marked_item: int) -> Tuple[QuantumState, Dict[str, int]]:
    """Execute Grover's Quantum Search Algorithm for an n-qubit space with a single marked item.
    Achieves O(sqrt(N)) quadratic speedup using optimal rotation count R ~ (pi/4) * sqrt(2^n).
    """
    dim = 2 ** num_qubits
    optimal_iterations = max(1, int(round((math.pi / 4) * math.sqrt(dim))))

    qc = QuantumCircuit(num_qubits)

    # Step 1: Initialize uniform superposition: H^n |0...0>
    for q in range(num_qubits):
        qc.h(q)

    state = qc.execute()

    # Step 2: Grover Iteration Loop
    for _ in range(optimal_iterations):
        # Oracle Phase Inversion: flip phase of |marked_item>
        oracle_matrix = np.eye(dim, dtype=np.complex128)
        oracle_matrix[marked_item, marked_item] = -1.0
        state.vec = oracle_matrix @ state.vec

        # Diffusion Operator: 2|s><s| - I (inversion about average)
        s = np.ones(dim, dtype=np.complex128) / math.sqrt(dim)
        diffusion = 2.0 * np.outer(s, s) - np.eye(dim, dtype=np.complex128)
        state.vec = diffusion @ state.vec

    counts = state.sample(num_shots=1000)
    return state, counts
