"""Comprehensive Test Suite for Quanta-Core Quantum Simulation Engine."""

import pytest
import numpy as np
import math
from quanta import QuantumState, QuantumCircuit, DensityMatrix, gates
from quanta.algorithms import create_bell_state, run_quantum_teleportation, grovers_algorithm

def test_ground_state_initialization():
    state = QuantumState(3)
    assert state.num_qubits == 3
    assert state.dim == 8
    assert np.isclose(state.vec[0], 1.0)
    assert np.isclose(np.linalg.norm(state.vec), 1.0)

def test_hadamard_superposition():
    qc = QuantumCircuit(1)
    qc.h(0)
    state = qc.execute()
    expected = (1 / np.sqrt(2)) * np.array([1.0, 1.0])
    assert np.allclose(state.vec, expected)
    probs = state.probabilities
    assert np.isclose(probs[0], 0.5)
    assert np.isclose(probs[1], 0.5)

def test_pauli_algebra():
    # X^2 = I, Y^2 = I, Z^2 = I, X Y = i Z
    assert np.allclose(gates.X @ gates.X, gates.I2)
    assert np.allclose(gates.Y @ gates.Y, gates.I2)
    assert np.allclose(gates.Z @ gates.Z, gates.I2)
    assert np.allclose(gates.X @ gates.Y, 1j * gates.Z)

def test_cnot_logic():
    qc = QuantumCircuit(2)
    qc.x(0)  # |10>
    qc.cx(0, 1)  # should flip target -> |11>
    state = qc.execute()
    assert np.isclose(state.vec[3], 1.0)  # idx 3 is |11>

def test_toffoli_logic():
    qc = QuantumCircuit(3)
    qc.x(0)
    qc.x(1)  # |110>
    qc.toffoli(0, 1, 2)  # target q2 should flip -> |111>
    state = qc.execute()
    assert np.isclose(state.vec[7], 1.0)  # idx 7 is |111>

def test_bell_state_entanglement():
    state = create_bell_state("phi_plus")
    probs = state.probabilities
    assert np.isclose(probs[0], 0.5)  # |00>
    assert np.isclose(probs[1], 0.0)  # |01>
    assert np.isclose(probs[2], 0.0)  # |10>
    assert np.isclose(probs[3], 0.5)  # |11>

def test_quantum_teleportation():
    # Test teleportation of arbitrary state with random phases
    for (a, b) in [(1.0, 0.0), (0.0, 1.0), (0.6, 0.8), (1/np.sqrt(2), 1j/np.sqrt(2))]:
        res = run_quantum_teleportation(a, b)
        assert res["success"] is True
        assert np.isclose(res["bob_fidelity"], 1.0, atol=1e-5)

def test_grovers_algorithm():
    # In a 3-qubit space (N=8), target item should have > 90% probability
    for target in [0, 3, 5, 7]:
        state, counts = grovers_algorithm(num_qubits=3, marked_item=target)
        probs = state.probabilities
        assert probs[target] > 0.90

def test_density_matrix_purity_and_entropy():
    # Pure state
    vec = np.array([1.0, 0.0], dtype=complex)
    dm = DensityMatrix.from_pure_state(vec)
    assert dm.is_pure is True
    assert np.isclose(dm.purity, 1.0)
    assert np.isclose(dm.von_neumann_entropy(), 0.0, atol=1e-6)

    # Maximally mixed state
    mixed = dm.apply_depolarizing_channel(1.0)
    assert np.isclose(mixed.purity, 0.5)
    assert np.isclose(mixed.von_neumann_entropy(), 1.0, atol=1e-6)

def test_bloch_coordinates():
    # |0> points to +Z (0, 0, 1)
    s0 = QuantumState(1)
    x, y, z = s0.bloch_coordinates(0)
    assert np.allclose([x, y, z], [0.0, 0.0, 1.0], atol=1e-4)

    # |+> points to +X (1, 0, 0)
    qc = QuantumCircuit(1)
    qc.h(0)
    s_plus = qc.execute()
    x, y, z = s_plus.bloch_coordinates(0)
    assert np.allclose([x, y, z], [1.0, 0.0, 0.0], atol=1e-4)

def test_circuit_draw():
    qc = QuantumCircuit(2)
    qc.h(0).cx(0, 1)
    diagram = qc.draw()
    assert "q0: |0>" in diagram
    assert "[H]" in diagram
    assert "●" in diagram
    assert "⊕" in diagram
