# Worked synthetic calculations

For target [a,b] and panel [c,d], K1=[a−d,b−c], K2=[c−b,d−a]; K3=[−L+,−L−]. V if upper<0; A if lower≥0; otherwise I. Any V persists; only all A gives joint A.

**Case A**

```json
{
  "case": "A",
  "change": null,
  "indetermination_reasons": {
    "K1": null,
    "K2": "sediment: sediment unavailable",
    "K3": "eligible interval spans the decision boundary"
  },
  "joint": "V",
  "margins": {
    "K1": [
      "-12",
      "-4"
    ],
    "K2": null,
    "K3": [
      "-0.3",
      "0"
    ]
  },
  "profile": [
    "V",
    "I",
    "I"
  ],
  "rate": null,
  "temporal_missing_reason": "baseline stock not supplied",
  "units": {
    "K1": "Mg C ha^-1",
    "K2": "Mg ha^-1 over (4,5]",
    "K3": "ha over [0,5]",
    "change": "Mg C ha^-1",
    "rate": "Mg C ha^-1 yr^-1"
  }
}
```

**Case B**

```json
{
  "case": "B",
  "change": null,
  "indetermination_reasons": {
    "K1": null,
    "K2": null,
    "K3": "eligible interval spans the decision boundary"
  },
  "joint": "I",
  "margins": {
    "K1": [
      "2",
      "10"
    ],
    "K2": [
      "0.4",
      "1"
    ],
    "K3": [
      "-0.3",
      "0"
    ]
  },
  "profile": [
    "A",
    "A",
    "I"
  ],
  "rate": null,
  "temporal_missing_reason": "baseline stock not supplied",
  "units": {
    "K1": "Mg C ha^-1",
    "K2": "Mg ha^-1 over (4,5]",
    "K3": "ha over [0,5]",
    "change": "Mg C ha^-1",
    "rate": "Mg C ha^-1 yr^-1"
  }
}
```

**Case C**

```json
{
  "case": "C",
  "change": null,
  "indetermination_reasons": {
    "K1": null,
    "K2": null,
    "K3": null
  },
  "joint": "V",
  "margins": {
    "K1": [
      "2",
      "10"
    ],
    "K2": [
      "0.4",
      "1"
    ],
    "K3": [
      "-0.6",
      "-0.4"
    ]
  },
  "profile": [
    "A",
    "A",
    "V"
  ],
  "rate": null,
  "temporal_missing_reason": "baseline stock not supplied",
  "units": {
    "K1": "Mg C ha^-1",
    "K2": "Mg ha^-1 over (4,5]",
    "K3": "ha over [0,5]",
    "change": "Mg C ha^-1",
    "rate": "Mg C ha^-1 yr^-1"
  }
}
```

**Case D**

```json
{
  "case": "D",
  "change": [
    "6",
    "12"
  ],
  "indetermination_reasons": {
    "K1": null,
    "K2": null,
    "K3": "eligible interval spans the decision boundary"
  },
  "joint": "V",
  "margins": {
    "K1": [
      "-12",
      "-4"
    ],
    "K2": [
      "0.4",
      "1"
    ],
    "K3": [
      "-0.3",
      "0"
    ]
  },
  "profile": [
    "V",
    "A",
    "I"
  ],
  "rate": [
    "1.2",
    "2.4"
  ],
  "temporal_missing_reason": null,
  "units": {
    "K1": "Mg C ha^-1",
    "K2": "Mg ha^-1 over (4,5]",
    "K3": "ha over [0,5]",
    "change": "Mg C ha^-1",
    "rate": "Mg C ha^-1 yr^-1"
  }
}
```

**Case E**

```json
{
  "case": "E",
  "change": [
    "-10",
    "-4"
  ],
  "indetermination_reasons": {
    "K1": null,
    "K2": null,
    "K3": "eligible interval spans the decision boundary"
  },
  "joint": "I",
  "margins": {
    "K1": [
      "2",
      "10"
    ],
    "K2": [
      "0.4",
      "1"
    ],
    "K3": [
      "-0.3",
      "0"
    ]
  },
  "profile": [
    "A",
    "A",
    "I"
  ],
  "rate": [
    "-2",
    "-0.8"
  ],
  "temporal_missing_reason": null,
  "units": {
    "K1": "Mg C ha^-1",
    "K2": "Mg ha^-1 over (4,5]",
    "K3": "ha over [0,5]",
    "change": "Mg C ha^-1",
    "rate": "Mg C ha^-1 yr^-1"
  }
}
```

D change=[42−36,46−34]=[6,12]; division by5 gives[1.2,2.4]. E change=[56−66,60−64]=[−10,−4]; division by5 gives[−2.0,−0.8]. No baseline for A/B/C means no temporal output. All component bounds are assumed, with no coverage claim. For q strata:2q+1 criteria,4q+1 unique quantities; h additional baseline stocks yield4q+1+h. These are component counts, not sample sizes or independence assumptions.
