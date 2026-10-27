"""Quantum State Vector and Hilbert Space Mathematics.

Implements pure statevector evolution in 2^n dimensional complex Hilbert space.
"""

from __future__ import annotations
import math
import cmath
from typing import List, Tuple, Dict, Optional
import numpy as np


class QuantumState:
    """Represents an n-qubit pure statevector in a 2^n complex Hilbert space."""

    def __init__(self, num_qubits: int, statevector: Optional[np.ndarray] = None):
        if num_qubits < 1 or num_qubits > 20:
            raise ValueError("Number of qubits must be between 1 and 20.")
        self.num_qubits = num_qubits
        self.dim = 2 ** num_qubits

        if statevector is None:
            # Default to ground state |0...0>
            self.vec = np.zeros(self.dim, dtype=np.complex128)
            self.vec[0] = 1.0 + 0.0j
        else:
            if len(statevector) != self.dim:
                raise ValueError(f"Statevector size {len(statevector)} does not match dimension 2^{num_qubits} = {self.dim}")
            self.vec = np.array(statevector, dtype=np.complex128)
            self.normalize()

    def normalize(self) -> None:
        """Normalize the statevector to unit norm <psi|psi> = 1."""
        norm = np.linalg.norm(self.vec)
        if norm < 1e-15:
            raise ValueError("Cannot normalize null statevector.")
        self.vec = self.vec / norm

    @property
    def probabilities(self) -> np.ndarray:
        """Born rule: P(i) = |<i|psi>|^2."""
        return np.abs(self.vec) ** 2

    def sample(self, num_shots: int = 1024, rng: Optional[np.random.Generator] = None) -> Dict[str, int]:
        """Sample classical outcomes from the probability distribution."""
        if rng is None:
            rng = np.random.default_rng()
        probs = self.probabilities
        outcomes = rng.choice(self.dim, size=num_shots, p=probs)
        counts: Dict[str, int] = {}
        fmt = f"0{self.num_qubits}b"
        for out in outcomes:
            bitstring = format(out, fmt)
            counts[bitstring] = counts.get(bitstring, 0) + 1
        return counts

    def measure_qubit(self, target_qubit: int, rng: Optional[np.random.Generator] = None) -> Tuple[int, QuantumState]:
        """Perform projective measurement on a single qubit, collapsing the state."""
        if rng is None:
            rng = np.random.default_rng()
        if target_qubit < 0 or target_qubit >= self.num_qubits:
            raise IndexError("Target qubit out of bounds.")

        # Compute probability of target qubit being 0
        p0 = 0.0
        shift = self.num_qubits - 1 - target_qubit
        for idx in range(self.dim):
            if not ((idx >> shift) & 1):
                p0 += abs(self.vec[idx]) ** 2

        p0 = max(0.0, min(1.0, p0))
        outcome = 0 if rng.random() < p0 else 1

        # Project state
        new_vec = np.zeros_like(self.vec)
        for idx in range(self.dim):
            bit = (idx >> shift) & 1
            if bit == outcome:
                new_vec[idx] = self.vec[idx]

        norm = np.linalg.norm(new_vec)
        if norm > 1e-15:
            new_vec /= norm

        self.vec = new_vec
        return outcome, self

    def fidelity(self, other: QuantumState) -> float:
        """Compute state fidelity F = |<psi|phi>|^2."""
        if self.num_qubits != other.num_qubits:
            raise ValueError("Cannot compute fidelity between states of different qubit counts.")
        inner_product = np.vdot(self.vec, other.vec)
        return float(abs(inner_product) ** 2)

    def bloch_coordinates(self, qubit_idx: int = 0) -> Tuple[float, float, float]:
        """Compute Bloch sphere vector coordinates (x, y, z) for single qubit reduced state."""
        rho = self.reduced_density_matrix([qubit_idx])
        sx = np.array([[0, 1], [1, 0]], dtype=complex)
        sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
        sz = np.array([[1, 0], [0, -1]], dtype=complex)

        x = float(np.real(np.trace(rho @ sx)))
        y = float(np.real(np.trace(rho @ sy)))
        z = float(np.real(np.trace(rho @ sz)))
        return x, y, z

    def reduced_density_matrix(self, keep_qubits: List[int]) -> np.ndarray:
        """Partial trace over discarded qubits to compute reduced density matrix rho_keep."""
        n = self.num_qubits
        k = len(keep_qubits)
        keep_qubits = sorted(keep_qubits)
        discard_qubits = [q for q in range(n) if q not in keep_qubits]

        full_rho = np.outer(self.vec, np.conj(self.vec)).reshape([2] * (2 * n))
        current_rho = full_rho
        for q in reversed(discard_qubits):
            current_rho = np.trace(current_rho, axis1=q, axis2=q + n)
            n -= 1

        dim_k = 2 ** k
        return current_rho.reshape((dim_k, dim_k))

    def __repr__(self) -> str:
        terms = []
        fmt = f"0{self.num_qubits}b"
        for i, amp in enumerate(self.vec):
            if abs(amp) > 1e-4:
                mag = abs(amp)
                phase = cmath.phase(amp)
                bit = format(i, fmt)
                if abs(phase) < 1e-4:
                    terms.append(f"{amp.real:+.3f}|{bit}>")
                else:
                    terms.append(f"({amp.real:+.2f}{amp.imag:+.2f}j)|{bit}>")
        state_str = " ".join(terms) if terms else "0"
        return f"QuantumState(qubits={self.num_qubits}, state={state_str})"
