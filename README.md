# Matching ecological indicator claims to evidence in grazing assessment

Reproducibility materials for the companion Viewpoint, **version 1.2.1**.

The Viewpoint asks how ecological claims can remain aligned with the evidence that supports them. It proposes an interpretation contract that keeps three questions distinct: how a site compares with a contemporary benchmark, how its condition changes over time, and whether an adopted no-conversion safeguard is fulfilled. This repository makes the demonstration inspectable through five synthetic cases, exact interval calculations, executable tests, and the source for Figure 1.

The cases show how increasing soil carbon can coexist with a current comparative deficit, and how favorable soil comparisons can leave conversion unresolved. They demonstrate the specified rule behavior under assumed bounds; they do not provide field validation.

**Version DOI:** [10.5281/zenodo.23483050](https://doi.org/10.5281/zenodo.23483050) · **[Archived release](https://github.com/MikeJorge/grazing-ecological-evidence-reproducibility/releases/tag/ei-v1.2.1-reproducibility)** · **[Figure 1](outputs/Figure_1.pdf)** · **[Worked calculations](docs/worked_calculations.md)**

## Scientific logic

The hypothetical grazing assessment combines two contemporary soil comparisons with a separately adopted safeguard against actual gross native-vegetation conversion. A margin is oriented so that a nonnegative value satisfies its criterion.

| Criterion | Margin and support | Question addressed |
|---|---|---|
| **K1 — soil carbon** | Target minus contemporary panel stock, in Mg C ha⁻¹, on fixed equivalent soil mass corresponding to nominal 0–30 cm. | Does current stock meet the specified comparative benchmark? |
| **K2 — sediment export** | Contemporary panel minus target export, in Mg ha⁻¹, at representative plot outlets over the complete concurrent window (4, 5]. | Is export no greater than the specified comparative benchmark? |
| **K3 — conversion safeguard** | Negative actual gross conversion, in ha, of baseline-native vegetation within a fixed property boundary over [0, 5]. Each converted location is counted once. | Is the adopted exact-zero conversion condition fulfilled? |

The panel is a prespecified compatible contemporary mean. It is neither a causal counterfactual nor a recovery target. For K3, regrowth, gains elsewhere, and boundary shrinkage cannot offset actual gross conversion. The criteria are author-selected necessary conditions for this limited joint claim; they do not define universal ecological adequacy. The complete definitions and temporal supports are in [the protocol](config/protocol.json).

For a **valid, eligible margin interval** [l, u], the evidentiary conclusions are:

- **A — evidence-supported satisfaction:** l ≥ 0.
- **V — evidence-supported nonfulfillment:** u < 0.
- **I — indetermination:** the interval includes negative and nonnegative values. Missing or ineligible evidence also remains I, with its reason retained.

Equality satisfies the criterion: [0, 0] supports A, whereas a negative lower bound with an upper bound of zero remains I. Invalid records stop the calculation for correction; they are not classified as ecological I. Exact duplicates add no weight, and conflicting duplicates halt execution.

For the complete prespecified critical set, **any valid V gives joint V; all required criteria must be A for joint A; otherwise the joint result is I**. The full criterion profile and reasons for I accompany that result. Temporal stock change is reported separately and never becomes a fourth criterion. No tolerance, compensatory score, or zero imputation is introduced.

## What the five cases show

These are alternative synthetic thought experiments for one stratum, not five farms or field replicates. Profiles are ordered K1 / K2 / K3; the case labels A–E are distinct from the conclusion symbol A.

| Case | Criterion profile | Joint result | Interpretation demonstrated |
|---|---|---|---|
| A | V / I / I | V | Missing sediment evidence does not erase supported nonfulfillment of the carbon criterion. |
| B | A / A / I | I | Favorable soil comparisons leave actual conversion unresolved. |
| C | A / A / V | V | Favorable soil comparisons cannot satisfy a joint claim when conversion violates the adopted safeguard. |
| D | V / A / I | V | A positive stock change can coexist with a current deficit relative to the panel. |
| E | A / A / I | I | Current stock can exceed the panel benchmark despite a negative stock change. |

None of the five cases yields joint A. K3 requires evidence supporting exactly zero actual gross conversion; a zero detection or favorable soil result does not establish that condition. The Supplementary Information discusses the separate symbolic joint-A boundary example and its qualifications. [Expected results](expected/table1_expected.json) and [worked calculations](docs/worked_calculations.md) provide the complete margins, changes, rates, and reasons.

## Reproduce version 1.2.1

Download and extract [EI_REPRODUCIBILITY_PACKAGE_v1.2.1.zip](https://github.com/MikeJorge/grazing-ecological-evidence-reproducibility/releases/download/ei-v1.2.1-reproducibility/EI_REPRODUCIBILITY_PACKAGE_v1.2.1.zip) for the archived version. The reference environment is Linux with **Python 3.12.14** and the exact dependencies in [requirements.lock](requirements.lock). From the extracted package root, the POSIX-shell setup is:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.lock
python reproduce_all.py
```

Use a Python 3.12.14 interpreter for the first command. If the recorded dependencies are already installed, run only `python reproduce_all.py`. Installation may require network access; reproduction itself needs no credentials, network lookup, or external data. [Detailed reproduction notes](docs/reproduction.md) describe the verification environment and its limitations.

The runner fixes locale, timezone, hash seed, and rendering backend. A successful run:

1. Recomputes the five cases and checks margins, profiles, joint conclusions, changes, and rates against independently transcribed expected results.
2. Passes **25 existing unit-test methods**.
3. Regenerates **18 numerical and figure files**, including standard, grayscale, and three color-vision versions of Figure 1.

For numerical reproduction alone, `python src/reproduce.py --out outputs` uses only the Python standard library. The existing verification record establishes byte-identical reproduction in the recorded installed environment; a fresh installation from a package index has not been retested here.

## Verification map

| To inspect | Files and connection to the manuscript |
|---|---|
| Assumptions and eligibility | [Synthetic inputs](data/synthetic_inputs.json), [protocol](config/protocol.json), and [schemas](schema/). |
| Numerical implementation | [Calculation source](src/reproduce.py) and [unit tests](tests/test_rules.py). The implementation checks both structure and semantics without an external JSON Schema engine. |
| Case results | [Expected values](expected/table1_expected.json), [computed JSON](outputs/results.json), and [table1.csv](outputs/table1.csv). The retained machine filename supplies **manuscript Table 2 and SI Table S2**, not the interpretation-contract Table 1. |
| Figure generation | [Python source](figures/figure1.py), [configuration](config/figure1.json), and [figure outputs](outputs/). The [PDF](outputs/Figure_1.pdf) is the vector master; [SVG](outputs/Figure_1.svg) is a companion and [PNG](outputs/Figure_1.png) is the 300-dpi review copy. |
| Accessible figure description | [Text equivalent of Figure 1](docs/figure_descriptions.md). Meaning is carried by labels and symbols as well as color. |
| Environment and integrity | [Recorded environment](environment.json), [locked dependencies](requirements.lock), and [SHA-256 manifest](SHA256SUMS.txt). |

On systems with GNU `sha256sum`, run `sha256sum -c SHA256SUMS.txt` **before reproduction** to check the supplied files. Rerunning may change runtime-specific paths in the figure layout report on another installation without changing the figure content. Each checkout or archive has its own matching manifest.

Figure 1 is generated from Python vector primitives and explicit JSON, without a source bitmap, tracing, manual image editing, or vector post-processing. The PNG is not the line-art raster master. Color-vision transformations are diagnostic previews, not accessibility certification.

## Scope of the evidence

All five cases use assumed interval bounds. The package supplies no field observations, fitted uncertainty model, assigned confidence level, or validated sampling coverage. Reproducing its arithmetic establishes implementation behavior within the stated protocol; it does not establish measurement validity, ecological adequacy, causal effects, practical usefulness, or superior decisions. The interpretation contract specifies reasoning and reporting rather than a new aggregation or inference rule. An equivalent fully specified dashboard would give the same conclusions.

Tests beyond cases A–E exercise algorithm behavior only. Altering a criterion, support, duration, uncertainty model, or protocol for another application requires separate justification. The companion Supplementary Information develops interval propagation, simultaneous claims, component counting, repeated-use limits, exact-zero qualifications, and the reusable interpretation-contract form. The manuscript and Supplementary Information are separate submission materials and are not included in this software archive.

## Version and provenance notes

This README was reorganized after release to improve navigation and explain the existing demonstration. **The scientific package remains v1.2.1.** The Git tag retains the original source snapshot. The release asset and existing Zenodo record receive only the authorized creator-name correction (given names: Michael Allim; family name: Jorge), with matching updated checksums; scientific files, version and DOI are unchanged. The default branch retains the later documentation update recorded in [CHANGELOG.md](CHANGELOG.md).

Two isolated builds of the final v1.2.1 implementation produced identical bytes for all 18 deterministic outputs. Those outputs also matched their historical v0.2.0 / canonical v1.2.0 counterparts. The v1.2.1 reporting correction derives temporal-unavailability reasons from the actual unavailable current-stock and baseline-stock records; its regression test changes neither criterion logic nor case A–E outputs.

The [version crosswalk](provenance/version_crosswalk.json) maps inherited `Supplementary Information v0.2.0` locators to the current SI. Its historical `release_status=NOT_RELEASED` records its pre-publication state; the DOI and versioned release above identify the published object. In the input JSON, `baseline_filename` is an anonymous source alias bound by `baseline_sha256`, not a claim that the original document is distributed here. Actual execution timestamps are provenance; the fixed figure build date of 2000-01-01 is rendering metadata, not an observation date.

## Citation

Jorge, M.A. (2026). *Matching ecological indicator claims to evidence in grazing assessment — reproducibility materials* (Version 1.2.1) [Computer software]. Zenodo. [https://doi.org/10.5281/zenodo.23483050](https://doi.org/10.5281/zenodo.23483050).

Machine-readable citation: [CITATION.cff](CITATION.cff). Archival metadata: [metadata/zenodo.json](metadata/zenodo.json). The DOI identifies the versioned reproducibility archive; it is not a manuscript DOI.

## Licenses

Copyright © 2026 Michael Allim Jorge for original package materials.

- **Original Python code and tests:** [MIT](LICENSE-CODE).
- **Original synthetic data, configuration, documentation, and author-created figure outputs:** [CC BY 4.0](LICENSE-DATA-DOCS).

These licenses apply to separate file categories. [File-level rights](metadata/file_rights.json) and [NOTICE.md](NOTICE.md) specify scope, method attribution, and retained third-party notices. Dependencies are installed separately; source fonts and private review records are not bundled.
