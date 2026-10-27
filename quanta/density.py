"""Density Matrix Mechanics, von Neumann Entropy, and Open Quantum Systems.

Supports mixed state dynamics, purity calculations, and quantum noise channels
(depolarizing channel, phase-damping/dephasing channel, amplitude damping).
"""

import numpy as np
from typing import Tuple

class DensityMatrix:
    """Density operator rho for pure and mixed quantum states."""

    def __init__(self, matrix: np.ndarray):
        self.mat = np.array(matrix, dtype=np.complex128)
        self.dim = self.mat.shape[0]
        # Verify trace = 1
        tr = np.trace(self.mat)
        if abs(tr - 1.0) > 1e-4:
            self.mat = self.mat / tr

    @classmethod
    def from_pure_state(cls, statevector: np.ndarray) -> "DensityMatrix":
        vec = statevector.flatten()
        return cls(np.outer(vec, np.conj(vec)))

    @property
    def purity(self) -> float:
        """Purity gamma = Tr(rho^2). For pure states gamma = 1; mixed states gamma < 1."""
        return float(np.real(np.trace(self.mat @ self.mat)))

    @property
    def is_pure(self) -> bool:
        return abs(self.purity - 1.0) < 1e-5

    def von_neumann_entropy(self) -> float:
        """Calculate von Neumann entropy S(rho) = -Tr(rho * log2(rho)) = -sum(lambda_i * log2(lambda_i))."""
        eigenvals = np.linalg.eigvalsh(self.mat)
        entropy = 0.0
        for val in eigenvals:
            if val > 1e-12:
                entropy -= val * np.log2(val)
        return float(entropy)

    def apply_depolarizing_channel(self, p: float) -> "DensityMatrix":
        """Depolarizing noise channel: epsilon(rho) = (1 - p)*rho + p * I / d."""
        p = max(0.0, min(1.0, p))
        id_mat = np.eye(self.dim, dtype=np.complex128) / self.dim
        new_mat = (1.0 - p) * self.mat + p * id_mat
        return DensityMatrix(new_mat)

    def apply_phase_damping(self, gamma: float) -> "DensityMatrix":
        """Single-qubit dephasing / phase damping channel:
        E_0 = [[1, 0], [0, sqrt(1-gamma)]]
        E_1 = [[0, 0], [0, sqrt(gamma)]]
        """
        if self.dim != 2:
            raise ValueError("Phase damping is currently defined for single-qubit states.")
        gamma = max(0.0, min(1.0, gamma))
        E0 = np.array([[1.0, 0.0], [0.0, np.sqrt(1.0 - gamma)]], dtype=np.complex128)
        E1 = np.array([[0.0, 0.0], [0.0, np.sqrt(gamma)]], dtype=np.complex128)
        new_mat = E0 @ self.mat @ np.conj(E0).T + E1 @ self.mat @ np.conj(E1).T
        return DensityMatrix(new_mat)
