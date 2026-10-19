# Reproduction instructions

Use Python 3.12.14 and the exact versions in `requirements.lock`. In an environment containing those versions, execute from the repository root:

```bash
python reproduce_all.py
```

The command runs the calculation, 25 existing unit tests, and deterministic Python figure rendering. No network access is needed after the dependencies are installed. To install dependencies into a separate environment when package access is available:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.lock
python reproduce_all.py
```

The numerical core uses only the standard library. `outputs/table1.csv` corresponds to manuscript Table 2 and SI Table S2. The configuration, numerical source, expected results, tests and figure source are unchanged from the accepted v1.2.1 package. The 18 shipped outputs matched a new run byte for byte on 19 October 2026. That run used the existing exact dependency environment, an empty output directory and an isolated Matplotlib cache; it did not reinstall dependencies. Installing from a package index has not been retested here.

`SHA256SUMS.txt` describes the staged files before rerunning. Runtime-specific path metadata in the layout report can differ on another installation without implying different figure content. Dependencies and source fonts are not bundled.
