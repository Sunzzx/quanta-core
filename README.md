# Quanta-Core ⚛️

**High-Performance Quantum Computing & Statevector Simulation Engine from Pure Linear Algebra Primitives.**

`quanta-core` is an educational and research-grade quantum circuit simulation kernel built from foundational tensor algebra in $2^n$-dimensional complex Hilbert spaces ($\mathbb{C}^{2^n}$). It implements universal gate synthesis, entanglement metrics, open quantum system decoherence, and canonical quantum algorithms with zero heavy dependencies.

---

## 🌟 Theoretical & Mathematical Foundations

### 1. Statevector & Hilbert Space Formalism
An $n$-qubit pure quantum state $|\psi\rangle$ is represented as a complex vector in a $2^n$-dimensional Hilbert space:

$$|\psi\rangle = \sum_{i=0}^{2^n-1} c_i |i\rangle, \quad c_i \in \mathbb{C}, \quad \sum_{i=0}^{2^n-1} |c_i|^2 = 1$$

Under the Born rule, the probability of measuring the classical bitstring corresponding to basis state $|k\rangle$ is:

$$P(k) = |\langle k | \psi \rangle|^2 = |c_k|^2$$

### 2. Universal Gate Synthesis & Matrix Lifting
Single-qubit unitary operations $U \in SU(2)$ acting on qubit $j$ in an $n$-qubit system are lifted to full Hilbert space dimension $2^n \times 2^n$ via the Kronecker tensor product:

$$U^{(j)} = I^{\otimes j} \otimes U \otimes I^{\otimes (n - j - 1)}$$

Universal gates supported:
* **Pauli Gates**: $\sigma_x, \sigma_y, \sigma_z$
* **Hadamard**: $H = \frac{1}{\sqrt{2}} \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$
* **Phase & T Gates**: $S = \text{diag}(1, i)$, $T = \text{diag}(1, e^{i\pi/4})$
* **Arbitrary Rotations**: $R_x(\theta), R_y(\theta), R_z(\theta)$
* **Controlled Gates**: $CNOT$ (CX), Controlled-Z (CZ), and 3-qubit Toffoli ($CCX$).

### 3. Open Quantum Systems & von Neumann Entropy
For mixed states arising from environmental decoherence or subsystem entanglement, the system is represented by a density operator $\rho$:

$$\rho = \sum_k p_k |\psi_k\rangle\langle\psi_k|, \quad \text{Tr}(\rho) = 1$$

* **Purity**: $\gamma = \text{Tr}(\rho^2)$ ($\gamma = 1$ for pure states, $\gamma < 1$ for mixed states).
* **von Neumann Entropy**: $S(\rho) = -\text{Tr}(\rho \log_2 \rho) = -\sum_i \lambda_i \log_2 \lambda_i$.
* **Decoherence Channels**: Implemented Depolarizing and Phase Damping channels via Kraus operators:
  $$\mathcal{E}(\rho) = \sum_k E_k \rho E_k^\dagger$$

---

## 🚀 Canonical Algorithms Implemented

### 1. Quantum Teleportation Protocol
Transfers an unknown arbitrary quantum state $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$ from Alice to Bob using an EPR Bell pair and 2 classical bits of communication:
1. Alice and Bob share entangled pair: $|\Phi^+\rangle = \frac{|00\rangle + |11\rangle}{\sqrt{2}}$
2. Alice performs Bell-state measurement on her two qubits.
3. Alice transmits measurement bits $(m_0, m_1)$ over classical channel.
4. Bob applies correction $X^{m_1} Z^{m_0}$ to retrieve $|\psi\rangle$ with **100% state fidelity ($F = 1.000$)**.

### 2. Grover's Quantum Search Algorithm
Finds a marked item in an unstructured database of $N = 2^n$ items with quadratic speedup $O(\sqrt{N})$ over classical $O(N)$ brute-force search.
* Optimal iteration count:
  $$R \approx \left\lfloor \frac{\pi}{4} \sqrt{N} \right\rfloor$$
* Alternates Oracle phase inversion ($I - 2|w\rangle\langle w|$) and Diffusion operator ($2|s\rangle\langle s| - I$).

---

## ⚡ Quickstart

### Installation
```bash
git clone https://github.com/Sunzzx/quanta-core.git
cd quanta-core
pip install -e .
```

### Interactive CLI Demos
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

All algorithms and matrix representations are verified with 100% assertion coverage:

```bash
pytest -v
```

---

## 📄 License
MIT License. Authored by Ayush Kandwal (Sunzzx).
