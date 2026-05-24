"""
Example 1: Basic Circuit Execution with qedclib

Execute quantum circuits and retrieve measurement results.
This is the simplest use of qedclib — create circuits, run them,
and inspect the output counts.

Usage:
    python 01_basic_execution.py
"""

import qedclib

# --- Step 1: Initialize qedclib with the desired API ---

qedclib.initialize("qiskit")
ex = qedclib.execute

# --- Step 2: Set the execution target ---

ex.set_execution_target(backend_id="qasm_simulator")

# --- Step 3: Create some circuits ---

from qiskit import QuantumCircuit

# A simple GHZ state circuit
def make_ghz_circuit(n_qubits):
    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(0)
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)
    qc.measure(range(n_qubits), range(n_qubits))
    qc.name = f"ghz_{n_qubits}q"
    return qc

circuits = [make_ghz_circuit(n) for n in [3, 4, 5]]

# --- Step 4: Execute ---

job_id, result = ex.execute_circuits(circuits, num_shots=1000)

# --- Step 5: Inspect results ---

counts_list = result.get_counts()

for i, counts in enumerate(counts_list):
    total = sum(counts.values())
    print(f"\n{circuits[i].name} ({total} shots):")
    for bitstring, count in sorted(counts.items(), key=lambda x: -x[1])[:4]:
        print(f"  {bitstring}: {count} ({100*count/total:.1f}%)")
