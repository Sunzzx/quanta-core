# Quanta-Core ⚛️

[![CI](https://github.com/Sunzzx/quanta-core/actions/workflows/ci.yml/badge.svg)](https://github.com/Sunzzx/quanta-core/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Polar](https://img.shields.io/badge/Sponsor-Polar.sh-blue?logo=polar)](https://polar.sh)
[![Commercial License](https://img.shields.io/badge/Commercial-Stripe%20Checkout-success)](https://buy.stripe.com/test_7sYdRb3430Kb9Nx3LIabK00)

**High-Performance Quantum Computing & Statevector Simulation Engine from Pure Linear Algebra Primitives.**

`quanta-core` is an educational and research-grade quantum circuit simulation kernel built from foundational tensor algebra in $2^n$-dimensional complex Hilbert spaces ($\mathbb{C}^{2^n}$). It implements universal gate synthesis, entanglement metrics, open quantum system decoherence, projective measurements, and canonical quantum algorithms with zero heavy dependencies.

---

## 🏛️ High-Level System Architecture

```mermaid
flowchart TD
    subgraph API [Quantum Circuit API]
        QC[QuantumCircuit]
        Gates[Universal Gates: H, Pauli X/Y/Z, S, T, Rθ, CX, CZ, CCX]
        Algorithms[Canonical Protocols: Bell, Teleportation, Grover, Bloch]
    end

    subgraph Engine [Statevector Engine]
        State[QuantumState: \mathbb{C}^{2^N} Statevector]
        Lifting[Kronecker Tensor Matrix Lifter]
        Evolution[Unitary Gate Contraction: |ψ'⟩ = U |ψ⟩]
        Norm[Born Rule Normalization ⟨ψ|ψ⟩ = 1.0]
    end

    subgraph Information [Quantum Information & Open Systems]
        DM[DensityMatrix: ρ = |ψ⟩⟨ψ|]
        PartialTrace[Reduced Density Matrix: ρ_A = Tr_B ρ]
        Entropy[von Neumann Entropy: S = -Tr ρ log_2 ρ]
        Kraus[Decoherence Channels: Depolarizing, Dephasing]
    end

    subgraph Interface [CLI & Visualizer]
        Draw[ASCII Circuit Visualizer]
        Bloch[Bloch Sphere 3D Projection]
        Hist[Measurement Probability Histogram]
        Bench[High-Throughput Benchmark]
    end

    QC --> Lifting --> Evolution --> State
    State --> Norm
    State --> DM --> PartialTrace --> Entropy
    State --> Hist
    QC --> Draw
    State --> Bloch
```

---

## 🌟 Theoretical & Mathematical Foundations

### 1. Statevector & Hilbert Space Formalism
An $n$-qubit pure quantum state $|\psi\rangle$ is represented as a complex normalized vector in a $2^n$-dimensional Hilbert space $\mathcal{H} = (\mathbb{C}^2)^{\otimes n} \cong \mathbb{C}^{2^n}$:

$$|\psi\rangle = \sum_{i=0}^{2^n-1} c_i |i\rangle, \quad c_i \in \mathbb{C}, \quad \sum_{i=0}^{2^n-1} |c_i|^2 = 1$$

Under the Born rule, the probability of measuring the classical bitstring corresponding to basis state $|k\rangle$ is:

$$P(k) = |\langle k | \psi \rangle|^2 = |c_k|^2$$

### 2. Universal Gate Synthesis & Matrix Lifting
Single-qubit unitary operations $U \in SU(2)$ acting on qubit $j$ in an $n$-qubit system are lifted to full Hilbert space dimension $2^n \times 2^n$ via the Kronecker tensor product:

$$U^{(j)} = I^{\otimes j} \otimes U \otimes I^{\otimes (n - j - 1)}$$

Universal gates supported:
* **Pauli Gates**: $\sigma_x = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}, \; \sigma_y = \begin{pmatrix} 0 & -i \\ i & 0 \end{pmatrix}, \; \sigma_z = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$
* **Hadamard**: $H = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$
* **Phase & T Gates**: $S = \text{diag}(1, i)$, $T = \text{diag}(1, e^{i\pi/4})$
* **Arbitrary Rotations**: $R_x(\theta) = e^{-i\frac{\theta}{2}\sigma_x}$, $R_y(\theta) = e^{-i\frac{\theta}{2}\sigma_y}$, $R_z(\theta) = e^{-i\frac{\theta}{2}\sigma_z}$
* **Controlled Gates**: $CNOT$ ($CX$), Controlled-Z ($CZ$), and 3-qubit Toffoli ($CCX$).

### 3. Open Quantum Systems & von Neumann Entropy
For mixed states arising from environmental decoherence or subsystem entanglement, the system is represented by a density operator $\rho$:

$$\rho = \sum_k p_k |\psi_k\rangle\langle\psi_k|, \quad \text{Tr}(\rho) = 1$$

* **Purity**: $\gamma = \text{Tr}(\rho^2)$ ($\gamma = 1$ for pure states, $\gamma < 1$ for mixed states).
* **von Neumann Entanglement Entropy**:
  $$S(\rho) = -\text{Tr}(\rho \log_2 \rho) = -\sum_i \lambda_i \log_2 \lambda_i$$
* **Decoherence Channels**: Implemented Depolarizing and Phase Damping channels via Kraus operators:
  $$\mathcal{E}(\rho) = \sum_k E_k \rho E_k^\dagger$$

---

## 📊 Algorithmic Complexity Analysis

| Operation | Time Complexity | Memory Complexity | Quantum Invariant Guarantee |
| :--- | :--- | :--- | :--- |
| **State Initialization** | $\mathcal{O}(2^N)$ | $\mathcal{O}(2^N)$ complex128 | $\sum |c_i|^2 = 1.000000$ (Born normalization) |
| **Single-Qubit Gate Lift** | $\mathcal{O}(2^N)$ | $\mathcal{O}(2^{2N})$ or tensor slice | Strict Unitarity $U^\dagger U = I$ |
| **2-Qubit Entangling Gate (CX)** | $\mathcal{O}(2^N)$ | $\mathcal{O}(2^N)$ | Non-local entanglement injection |
| **Projective Measurement** | $\mathcal{O}(2^N)$ | $\mathcal{O}(1)$ | Wavefunction collapse per Born rule |
| **Reduced Density Matrix** | $\mathcal{O}(2^N)$ | $\mathcal{O}(2^{2N_A})$ | Hermiticity $\rho^\dagger = \rho$, $\text{Tr}(\rho)=1$ |
| **von Neumann Entropy** | $\mathcal{O}(d^3)$ ($d=2$) | $\mathcal{O}(d^2)$ | Invariance under local unitary transforms |
| **Quantum Teleportation** | $\mathcal{O}(1)$ gates | $\mathcal{O}(2^3) = 8$ states | Exact state recovery $\mathcal{F} = 1.000000$ |
| **Grover Search ($N=2^n$)** | $\mathcal{O}(\sqrt{N})$ oracle steps | $\mathcal{O}(N)$ amplitudes | Quadratic speedup, $>94\%$ recovery |

---

## 🚀 Canonical Algorithms Implemented

### 1. Quantum Teleportation Protocol (Bennett et al.)
Transfers an unknown arbitrary quantum state $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ from Alice to Bob using an EPR Bell pair and 2 classical bits of communication:
1. Alice and Bob share entangled pair: $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$
2. Alice performs Bell-state measurement on her two qubits.
3. Alice transmits measurement bits $(m_0, m_1)$ over classical channel.
4. Bob applies correction $X^{m_1} Z^{m_0}$ to retrieve $|\psi\rangle$ with **100% state fidelity ($\mathcal{F} = 1.000000$)**.

### 2. Grover's Quantum Search Algorithm
Finds a marked item in an unstructured database of $N = 2^n$ items with quadratic speedup $\mathcal{O}(\sqrt{N})$ over classical $\mathcal{O}(N)$ brute-force search.
* Optimal iteration count:
  $$R \approx \left\lfloor \frac{\pi}{4} \sqrt{N} \right\rfloor$$
* Alternates Oracle phase inversion ($I - 2|w\rangle\langle w|$) and Diffusion operator ($2|s\rangle\langle s| - I$).

---

## ⚡ Empirical Performance Benchmarks

Executed on Apple Silicon (M-series, Darwin) via `quanta benchmark`:

| Qubits ($N$) | Hilbert Dimension ($2^N$) | Circuit Gates | Execution Time | Gate Throughput |
| :---: | :---: | :---: | :---: | :---: |
| **2** | 4 | 5 | **1.10 ms** | ~4,541 gates/sec |
| **4** | 16 | 11 | **0.26 ms** | ~42,098 gates/sec |
| **6** | 64 | 17 | **1.23 ms** | ~13,769 gates/sec |
| **8** | 256 | 23 | **11.96 ms** | ~1,922 gates/sec |
| **10** | 1,024 | 29 | **235.50 ms** | ~123 gates/sec |

*Normalization Invariant Audit: 100% of tested circuits preserved $\langle\psi|\psi\rangle = 1.000000000000000$.*

---

## 🛠️ Quickstart & CLI Commands

### Installation
```bash
git clone https://github.com/Sunzzx/quanta-core.git
cd quanta-core
pip install -e .
```

### Run Benchmarks & Verifications
```bash
# Run statevector scaling throughput benchmark
quanta benchmark

# Run comprehensive test suite
quanta test
```

### Interactive Demos
```bash
# Run Bell Pair Entanglement Demo
quanta demo bell

# Run 3-Qubit Quantum Teleportation Protocol
quanta demo teleport

# Run Grover's Search Algorithm (Quadratic Speedup)
quanta demo grover

# Render Bloch Sphere Projection Coordinates
quanta demo bloch
```

### Python API
```python
from quanta import QuantumCircuit, QuantumState

# Construct Bell state circuit: (|00> + |11>) / sqrt(2)
qc = QuantumCircuit(2)
qc.h(0).cx(0, 1)

# Print ASCII Circuit
print(qc.draw())
# q0: |0> ──[H]──●──
# q1: |0> ───────⊕──

# Execute statevector evolution
state = qc.execute()
print(state)
# QuantumState(qubits=2, state=+0.707|00> +0.707|11>)

# Sample measurement distribution (Born rule)
counts = state.sample(num_shots=1000)
print(counts)
# {'00': 504, '11': 496}
```

---

## 🧪 Verification & Test Suite

Executed via `uv run pytest -v`:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.9, pytest-8.4.2
rootdir: /Users/ayu/Developer/quanta-core
collected 11 items

tests/test_quantum.py::test_ground_state_initialization PASSED           [  9%]
tests/test_quantum.py::test_hadamard_superposition PASSED                [ 18%]
tests/test_quantum.py::test_pauli_algebra PASSED                         [ 27%]
tests/test_quantum.py::test_cnot_logic PASSED                            [ 36%]
tests/test_quantum.py::test_toffoli_logic PASSED                         [ 45%]
tests/test_quantum.py::test_bell_state_entanglement PASSED               [ 54%]
tests/test_quantum.py::test_quantum_teleportation PASSED                 [ 63%]
tests/test_quantum.py::test_grovers_algorithm PASSED                     [ 72%]
tests/test_quantum.py::test_density_matrix_purity_and_entropy PASSED     [ 81%]
tests/test_quantum.py::test_bloch_coordinates PASSED                     [ 90%]
tests/test_quantum.py::test_circuit_draw PASSED                          [100%]

============================== 11 passed in 0.18s ==============================
```

---

## 💼 Commercial Licensing & Monetization

`quanta-core` is dual-licensed under open-source MIT for personal experimentation and research, with enterprise commercial licenses available for proprietary integration and high-performance quantum simulation deployments.

- **Commercial License ($99 USD single seat):** [Purchase via Stripe Checkout](https://buy.stripe.com/test_7sYdRb3430Kb9Nx3LIabK00)
- **Sponsor Development:** [Polar.sh Creator Funding](https://polar.sh)
- **Enterprise Support & Inquiries:** `ayushkandwal2007@gmail.com`

---

## 📄 License
MIT License. Authored by Ayush Kandwal (Sunzzx).
