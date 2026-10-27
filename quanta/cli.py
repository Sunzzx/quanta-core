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

    args = parser.parse_args()

    if args.command == "demo":
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
