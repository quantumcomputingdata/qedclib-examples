# qedclib-examples

Examples and applications using the [qedclib](https://pypi.org/project/qedclib/) quantum computing execution library.

## Installation

```bash
pip install qedclib
```

Or for development against the latest source:
```bash
git clone https://github.com/SRI-International/QC-App-Oriented-Benchmarks.git
cd QC-App-Oriented-Benchmarks
pip install -e .
```

## Examples

### basics/
Getting started with qedclib — configuring backends, running circuits, and retrieving results.

- **01_hello_circuit.py** — Minimal example: create a Bell state, execute on a simulator, print counts.
- **02_basic_execution.py** — Execute multiple circuits as a batch using `execute_circuits()` and inspect results. Shows the simplest path for running circuits without metrics overhead.
- **03_execution_with_metrics.py** — Full metrics-integrated execution using `submit_circuits()`. Demonstrates circuit grouping, custom result handlers for fidelity computation, automatic timing collection, and circuit depth metrics. This is the recommended pattern for applications that need performance data.

### backends/
Working with different execution targets — local simulators, IBM Quantum, IonQ, IQM — and switching between them.

- **04_hardware_execution.py** — Run circuits on real quantum hardware. Shows configuration patterns for IBM Quantum, IonQ, and IQM, with command-line backend selection. Defaults to local simulator for testing.

### applications/
Real-world use cases showing qedclib as a general-purpose execution engine with circuits from external sources.

- **05_external_circuits.py** — Execute circuits from [MQT Bench](https://mqt.readthedocs.io/projects/bench/) with qedclib metrics. Demonstrates the key pattern: bring circuits from any source, let qedclib handle execution, timing, and fidelity analysis. Requires `pip install mqt.bench`.

## Documentation

- [qedclib documentation](https://sri-international.github.io/QC-App-Oriented-Benchmarks/)
- [PyPI package](https://pypi.org/project/qedclib/)

## License

Apache-2.0
