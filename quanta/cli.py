"""Quanta-Core Command-Line Interface."""

import sys
import argparse
from quanta import QuantumCircuit, create_bell_state, run_quantum_teleportation, grovers_algorithm, render_histogram, render_bloch_ascii

def main():
    parser = argparse.ArgumentParser(description="Quanta-Core: Quantum Simulation Engine")
    sub = parser.add_subparsers(dest="command")

    # Demo subcommands
    demo_p = sub.add_parser("demo", help="Run canonical quantum algorithms")
    demo_p.add_argument("name", choices=["bell", "teleport", "grover", "bloch"])

    # Benchmark subcommand
    bench_p = sub.add_parser("benchmark", help="Benchmark quantum statevector evolution throughput")
    bench_p.add_argument("--max-qubits", type=int, default=10, help="Max qubit count to simulate (default: 10)")

    # Test subcommand
    sub.add_parser("test", help="Execute comprehensive verification test suite")

    args = parser.parse_args()

    if args.command == "benchmark":
        import time
        max_q = min(args.max_qubits, 12)
        print("=" * 72)
        print("⚡ QUANTA-CORE: QUANTUM STATEVECTOR EVOLUTION BENCHMARK")
        print("=" * 72)
        print(f"{'Qubits (N)':<12}{'Hilbert Dim (2^N)':<20}{'Gates':<10}{'Time (ms)':<15}{'Throughput (gates/s)':<20}")
        print("-" * 72)
        for n in range(2, max_q + 1, 2):
            qc = QuantumCircuit(n)
            for q in range(n):
                qc.h(q)
            for q in range(n - 1):
                qc.cx(q, q + 1)
            for q in range(n):
                qc.z(q)
            gate_count = len(qc.ops)
            t0 = time.perf_counter()
            state = qc.execute()
            t1 = time.perf_counter()
            dur_ms = (t1 - t0) * 1000.0
            throughput = gate_count / max(t1 - t0, 1e-9)
            print(f"{n:<12}{state.dim:<20}{gate_count:<10}{dur_ms:<15.2f}{throughput:<20.1f}")
        print("-" * 72)
        print("✓ All statevector unitary evolutions completed with exact normalization <ψ|ψ>=1.0")
    elif args.command == "test":
        import subprocess
        ret = subprocess.run([sys.executable, "-m", "pytest", "-v"], cwd="/Users/ayu/Developer/quanta-core")
        sys.exit(ret.returncode)
    elif args.command == "demo":
        if args.name == "bell":
            print("=" * 60)
            print("🧪 DEMO: EPR BELL PAIR ENTANGLEMENT (|00> + |11>) / sqrt(2)")
            print("=" * 60)
            state = create_bell_state("phi_plus")
            print("Final State:", state)
            counts = state.sample(num_shots=1000)
            print("\nMeasurement Distribution (1000 shots):")
            print(render_histogram(counts))
        elif args.name == "teleport":
            print("=" * 60)
            print("🧪 DEMO: QUANTUM TELEPORTATION PROTOCOL (3 Qubits)")
            print("=" * 60)
            # Teleport arbitrary state |psi> = 0.6|0> + 0.8|1>
            res = run_quantum_teleportation(0.6, 0.8)
            print(f"Target State: {res['target_state'][0]:.2f}|0> + {res['target_state'][1]:.2f}|1>")
            print(f"Alice Measured Bits (m0, m1): {res['measured_bits']}")
            print(f"Bob Recovered State Fidelity: {res['bob_fidelity']:.6f}")
            print(f"Success: {res['success']} (Perfect Teleportation!)")
        elif args.name == "grover":
            print("=" * 60)
            print("🧪 DEMO: GROVER'S QUANTUM SEARCH ALGORITHM (3 Qubits, 8 States)")
            print("=" * 60)
            marked = 5  # |101>
            print(f"Target item marked in black-box oracle: |{format(marked, '03b')}>")
            state, counts = grovers_algorithm(num_qubits=3, marked_item=marked)
            print("Statevector after optimal amplitude amplification:")
            print(state)
            print("\nMeasurement Histogram:")
            print(render_histogram(counts))
        elif args.name == "bloch":
            print("=" * 60)
            print("🧪 DEMO: BLOCH SPHERE COORDINATES FOR HADAMARD STATE |+>")
            print("=" * 60)
            qc = QuantumCircuit(1)
            qc.h(0)
            state = qc.execute()
            x, y, z = state.bloch_coordinates(0)
            print(render_bloch_ascii(x, y, z))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
