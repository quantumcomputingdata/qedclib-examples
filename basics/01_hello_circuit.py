"""
01_hello_circuit.py — Minimal qedclib example

Creates a Bell state circuit, executes it on a local simulator,
and prints the measurement results.

Prerequisites:
    pip install qedclib qiskit qiskit-aer
"""

import qedclib
from qiskit import QuantumCircuit

# Initialize qedclib with Qiskit
qedclib.initialize("qiskit")
ex = qedclib.execute

# Set up a local simulator
ex.set_execution_target(backend_id="qasm_simulator")

# Build a Bell state circuit
qc = QuantumCircuit(2, 2, name="bell")
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Execute and print results
job_id, result = ex.execute_circuits([qc], num_shots=1000)
counts = result.get_counts()
print(f"Bell state counts: {counts}")
