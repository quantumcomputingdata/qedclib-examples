"""
Example 5: Execute External Circuits with qedclib Metrics

Demonstrates using qedclib to execute circuits from an external source
(MQT Bench) with full metrics collection. This shows qedclib's role as
a general-purpose execution engine — you bring the circuits from any
source, qedclib handles execution, timing, and performance analysis.

The pattern:
    1. Get circuits from any source (MQT Bench, Qiskit, hand-built, etc.)
    2. Organize them as {group: {circuit_id: circuit}}
    3. Use submit_circuits() for automatic metrics collection
    4. Retrieve and analyze the results

Prerequisites:
    pip install qedclib qiskit qiskit-aer mqt.bench

Usage:
    python 05_external_circuits.py
    python 05_external_circuits.py --benchmark qnn --max_qubits 10
"""

import argparse
import qedclib
from qedclib import metrics

qedclib.initialize("qiskit")
ex = qedclib.execute

from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from mqt.bench import get_benchmark, BenchmarkLevel


# --- Step 1: Get circuits from MQT Bench ---

def get_mqt_circuits(benchmark_name, min_qubits, max_qubits, max_circuits=3):
    """Fetch circuits from MQT Bench, organized as qedclib groups."""
    circuits = {}
    for n_qubits in range(min_qubits, max_qubits + 1):
        group = str(n_qubits)
        circuits[group] = {}
        for idx in range(max_circuits):
            qc = get_benchmark(
                benchmark=benchmark_name,
                level=BenchmarkLevel.ALG,
                circuit_size=n_qubits
            )
            qc.name = f"{benchmark_name}_{n_qubits}q_{idx}"
            circuits[group][str(idx)] = qc
    return circuits


# --- Step 2: Define result handler for fidelity ---

def execution_handler(qc, result, num_qubits, circuit_id, num_shots):
    """Compare execution results against noiseless simulation."""
    # Run same circuit on noiseless simulator to get ideal distribution
    sim = Aer.get_backend("aer_simulator")
    tqc = transpile(qc, sim)
    ideal_counts = sim.run(tqc, shots=int(num_shots)).result().get_counts()

    # Compute fidelity between actual and ideal
    counts = result.get_counts()
    fidelity = metrics.polarization_fidelity(counts, ideal_counts)

    metrics.store_metric(num_qubits, circuit_id, "fidelity", fidelity)


# --- Step 3: Execute with metrics ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute MQT Bench circuits with qedclib")
    parser.add_argument("--benchmark", "-b", default="wstate",
                        help="MQT Bench algorithm (wstate, ghz, qnn, etc.)")
    parser.add_argument("--min_qubits", type=int, default=2)
    parser.add_argument("--max_qubits", type=int, default=8)
    parser.add_argument("--max_circuits", "-c", type=int, default=3)
    parser.add_argument("--num_shots", "-s", type=int, default=1000)
    args = parser.parse_args()

    ex.set_execution_target(backend_id="qasm_simulator")

    # Fetch circuits from MQT Bench
    circuits = get_mqt_circuits(
        args.benchmark, args.min_qubits, args.max_qubits, args.max_circuits
    )
    total = sum(len(g) for g in circuits.values())
    print(f"Fetched {total} '{args.benchmark}' circuits from MQT Bench "
          f"({args.min_qubits}-{args.max_qubits} qubits)\n")

    # Initialize and execute with full metrics
    metrics.init_metrics()
    ex.init_execution(execution_handler)
    ex.compute_all_circuit_metrics(circuits)
    ex.submit_circuits(circuits, num_shots=args.num_shots)
    metrics.finalize_all_groups()

    # Display results
    print("\n--- Results by qubit group ---")
    gm = metrics.get_group_metrics()
    print(f"  {'qubits':>6}  {'avg_fidelity':>12}  {'avg_depth':>10}  {'avg_exec':>10}")
    print(f"  {'------':>6}  {'------------':>12}  {'--------':>10}  {'--------':>10}")
    for i, group in enumerate(gm["groups"]):
        fid = gm["avg_fidelities"][i] if i < len(gm["avg_fidelities"]) else 0
        depth = gm["avg_depths"][i] if i < len(gm.get("avg_depths", [])) else "?"
        exec_t = gm["avg_exec_times"][i] if i < len(gm["avg_exec_times"]) else 0
        print(f"  {group:>6}  {fid:>12.3f}  {depth:>10}  {exec_t:>10.4f}s")
