"""
Example 3: Execution with Automatic Metrics Collection

Use submit_circuits() to execute circuits with automatic timing
and performance metrics. This is the recommended path when you
want both results and execution statistics.

Circuits are organized as a nested dict {group: {circuit_id: circuit}},
where groups typically correspond to qubit widths. Metrics are collected
per-circuit and aggregated per-group.

Usage:
    python 03_execution_with_metrics.py
"""

import qedclib
from qedclib import metrics

# --- Step 1: Initialize and configure ---

qedclib.initialize("qiskit")
ex = qedclib.execute

ex.set_execution_target(backend_id="qasm_simulator")

# --- Step 2: Create circuits organized by group ---
# The nested dict structure {group: {circuit_id: circuit}} is required
# by submit_circuits. Groups are typically qubit widths.

from qiskit import QuantumCircuit

def make_ghz_circuit(n_qubits, circuit_id):
    qc = QuantumCircuit(n_qubits, n_qubits)
    qc.h(0)
    for i in range(n_qubits - 1):
        qc.cx(i, i + 1)
    qc.measure(range(n_qubits), range(n_qubits))
    qc.name = f"ghz_{n_qubits}q_{circuit_id}"
    return qc

circuits = {}
for n_qubits in [4, 6, 8]:
    group = str(n_qubits)
    circuits[group] = {}
    for cid in range(3):  # 3 circuits per group
        circuits[group][str(cid)] = make_ghz_circuit(n_qubits, cid)

total = sum(len(g) for g in circuits.values())
print(f"Created {total} circuits in {len(circuits)} groups\n")

# --- Step 3: Define a result handler (optional) ---
# Called once per circuit after execution. Use it to compute
# application-specific metrics like fidelity.

def my_result_handler(qc, result, group, circuit_id, num_shots):
    counts = result.get_counts()
    n_qubits = int(group)
    # For GHZ, check how often we get all-zeros or all-ones
    ideal = counts.get('0' * n_qubits, 0) + counts.get('1' * n_qubits, 0)
    fidelity = ideal / num_shots
    metrics.store_metric(group, circuit_id, 'fidelity', fidelity)

# --- Step 4: Execute with metrics ---

ex.init_execution(my_result_handler)

# Initialize metrics before computing circuit info, so that
# submit_circuits doesn't re-initialize and clear the depth metrics
metrics.init_metrics()

# Optional: compute circuit depth/gate metrics before execution
ex.compute_all_circuit_metrics(circuits)

# Submit circuits — this calls execute_circuits internally, stores
# timing metrics, and invokes the result handler for each circuit
ex.submit_circuits(circuits, num_shots=1000)

# Finalize metrics aggregation
metrics.finalize_all_groups()

# --- Step 5: Retrieve and display metrics ---

print("--- Per-circuit metrics ---")
cm = metrics.get_circuit_metrics()
for group in sorted(cm, key=lambda g: int(g) if g.isdigit() else 0):
    if not isinstance(cm[group], dict):
        continue
    for cid in cm[group]:
        m = cm[group][cid]
        print(f"  group={group:>2} circuit={cid}: "
              f"fidelity={m.get('fidelity', '?'):>5.3f}  "
              f"exec_time={m.get('exec_time', 0):.4f}s  "
              f"depth={m.get('depth', '?')}")

print("\n--- Group averages ---")
gm = metrics.get_group_metrics()
for i, group in enumerate(gm["groups"]):
    print(f"  group={group:>2}: "
          f"avg_exec={gm['avg_exec_times'][i]:.4f}s  "
          f"avg_fidelity={gm['avg_fidelities'][i]:.3f}")
