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

### applications/
Real-world use cases: parameter sweeps for phase diagrams, variational circuits for ML, and other computational science workflows.

### backends/
Working with different execution targets — local simulators, IBM Quantum, IonQ, IQM — and switching between them.

## Documentation

- [qedclib documentation](https://sri-international.github.io/QC-App-Oriented-Benchmarks/)
- [PyPI package](https://pypi.org/project/qedclib/)

## License

Apache-2.0
