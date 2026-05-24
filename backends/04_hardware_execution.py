"""
Example 4: Executing on Hardware Backends

Demonstrates running circuits on real quantum hardware using qedclib.
Shows IBM Quantum, IonQ, and IQM configuration patterns.

Prerequisites:
    pip install qedclib qiskit qiskit-aer qiskit-ibm-runtime

For IBM: set environment variables IBM_API_TOKEN and IBM_INSTANCE.
For IonQ: pip install qiskit-ionq and set IONQ_API_KEY.
For IQM: pip install iqm-qiskit and set IQM_API_TOKEN.

Usage:
    python 04_hardware_execution.py              # runs on simulator (default)
    python 04_hardware_execution.py --backend ibm_sherbrooke
    python 04_hardware_execution.py --backend ionq_simulator
"""

import argparse
import qedclib
from qedclib import metrics

qedclib.initialize("qiskit")
ex = qedclib.execute

from qiskit import QuantumCircuit


# --- Build test circuits ---

def make_ghz_circuit(n_qubits):
    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(0)
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)
    qc.measure(range(n_qubits), range(n_qubits))
    qc.name = f"ghz_{n_qubits}q"
    return qc


# --- Configure backend ---

def configure_backend(backend_id):
    """Set up execution target based on backend name."""

    if backend_id.startswith("ibm"):
        import os
        ibm_instance = os.environ.get("IBM_INSTANCE", "")
        ex.set_execution_target(
            backend_id=backend_id,
            hub="", group="", project=ibm_instance,
            exec_options={"use_ibm_quantum_platform": False, "use_sessions": False}
        )

    elif backend_id.startswith("ionq"):
        from qiskit_ionq import IonQProvider
        provider = IonQProvider()
        ionq_backend = provider.get_backend(backend_id)
        ex.set_execution_target(backend_id=backend_id, provider_backend=ionq_backend)

    elif backend_id.startswith("iqm"):
        from iqm.qiskit_iqm import IQMProvider
        import os
        provider = IQMProvider(
            "https://resonance.meetiqm.com",
            quantum_computer="garnet",
            token=os.environ.get("IQM_API_TOKEN")
        )
        ex.set_execution_target(backend_id="garnet", provider_backend=provider.get_backend())

    else:
        # Local simulator
        ex.set_execution_target(backend_id=backend_id)


# --- Main ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute circuits on a quantum backend")
    parser.add_argument("--backend", "-b", default="qasm_simulator", help="Backend name")
    parser.add_argument("--num_shots", "-s", type=int, default=1000, help="Shots per circuit")
    parser.add_argument("--max_qubits", "-max", type=int, default=6, help="Max qubits")
    args = parser.parse_args()

    configure_backend(args.backend)

    circuits = [make_ghz_circuit(n) for n in range(2, args.max_qubits + 1)]
    print(f"Executing {len(circuits)} circuits on {args.backend}")

    job_id, result = ex.execute_circuits(circuits, num_shots=args.num_shots)

    counts_list = result.get_counts()
    for i, counts in enumerate(counts_list):
        total = sum(counts.values())
        top = sorted(counts.items(), key=lambda x: -x[1])[:3]
        print(f"\n{circuits[i].name}:")
        for bitstring, count in top:
            print(f"  {bitstring}: {count} ({100*count/total:.1f}%)")
