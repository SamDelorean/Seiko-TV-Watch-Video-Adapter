# Pin-6 Waveform Hypothesis Matrix — V0.1

Status: **expanded waveform-family test plan; no wrist connection allowed**

## Purpose

The Seiko pin-6 uncertainty is not only "gain or no gain."

At least four materially different waveform families must be considered:

1. positive-going picture above a DC operating point;
2. negative-going picture below a DC operating point;
3. bipolar picture centered around a DC operating point;
4. large ground-referenced/full-scale picture swing, e.g. approximately 0 to 8 V.

These are different hypotheses and must be tested independently.

The correct design variables are:

```text
A. amplitude / gain
B. polarity
C. DC anchor / centering
```

Do not change all three at once during characterization.

---

## 1. Normalized source variable

Define normalized picture luminance:

```text
x = 0 -> black
x = 1 -> white
```

The source-side `VIDEO_NORM` node is assumed to have sync removed and a stable black reference.

---

# FAMILY P+ — Positive unipolar excursion above offset

## Transfer

```text
VOUT = V0 + A*x
```

where:

- `V0` = DC black/reference level;
- `A` = black-to-white excursion.

### Example

For:

```text
V0 = 8.0 V
A  = 1.5 V
```

then:

```text
black = 8.0 V
50%   = 8.75 V
white = 9.5 V
```

## Interpretation

The reported "about 8 V plus video" could mean exactly this.

The 8-V point is the black/reference floor and increasing luminance moves upward.

## Warning

This mode can exceed the apparent 8-V operating level.

Do not assume the upper limit is safe merely because the reference is near 8 V.

---

# FAMILY P- — Negative unipolar excursion below offset

## Transfer

```text
VOUT = V0 - A*x
```

### Example

For:

```text
V0 = 8.0 V
A  = 1.5 V
```

then:

```text
black = 8.0 V
50%   = 7.25 V
white = 6.5 V
```

## Interpretation

The same reported operating point can support inverted picture polarity.

This is entirely plausible if the original receiver output stage or wrist input inverts the video relationship.

## Warning

Do not treat negative-going picture as "negative voltage."

The signal may remain entirely positive with respect to ground while moving downward from its DC bias.

---

# FAMILY P± — Bipolar excursion centered on offset

## Transfer

Use peak excursion `AP`:

```text
VOUT = V0 + AP*(2*x - 1)
```

This gives:

```text
black = V0 - AP
50%   = V0
white = V0 + AP
```

## Literal ±1.5-V interpretation

If the phrase means **±1.5 V around the offset**:

```text
V0 = 8.0 V
AP = 1.5 V
```

then:

```text
black = 6.5 V
50%   = 8.0 V
white = 9.5 V
total excursion = 3.0 Vpp
```

## Alternative 1.5-Vpp-centered interpretation

If historical measurements saying "about 1.5 V video excursion" meant **1.5 Vpp total**, then:

```text
AP = 0.75 V
```

and:

```text
black = 7.25 V
50%   = 8.0 V
white = 8.75 V
total excursion = 1.5 Vpp
```

Both versions must remain distinguishable until the original waveform is captured.

## Interpretation

This family means the reported ~8-V level is the **midpoint**, not black level.

That is fundamentally different from P+ and P-.

## Warning

This is currently considered less likely, but must not be discarded without a DC-coupled capture.

A scope screenshot centered by AC coupling could easily make a unipolar waveform look bipolar.

---

# FAMILY FS — Large ground-referenced/full-scale swing

## Transfer

First positive-polarity test:

```text
VOUT = VFS*x
```

Example:

```text
VFS = 8.0 V

black = 0 V
50%   = 4 V
white = 8 V
```

Optional inverted test if evidence requires it:

```text
VOUT = VFS*(1-x)
```

so:

```text
black = 8 V
white = 0 V
```

## Interpretation

This hypothesis treats the reported ~8 V not as an offset at all, but as approximately the top of a much larger video swing.

This would imply a very different original output-stage architecture.

## Warning

**This is the highest-risk linear hypothesis.**

Do not apply a 0-to-8-V or 8-to-0-V waveform to the wrist unit based only on secondary reports.

It must be tested into a dummy/high-impedance load only until original TR02-01 measurements explicitly support such a large swing.

---

## 2. Orthogonal amplitude question

Within P+ and P-, amplitude can still be:

```text
unity relative to normalized luma
or
amplified/attenuated
```

Therefore:

```text
P+ / unity
P+ / gain
P- / unity
P- / gain
```

are separate cases.

For P±, the relevant parameter is peak excursion around the midpoint.

For FS, the relevant parameter is the full-scale endpoint voltage.

This prevents "gain" from being confused with "polarity" or "centering."

---

## 3. Recommended test-mode selector

The bench should ultimately expose explicit modes:

```text
MODE 1  P+  black anchored at V0, positive-going
MODE 2  P-  black anchored at V0, negative-going
MODE 3A P±  centered, 1.5 Vpp total
MODE 3B P±  centered, ±1.5 V (3.0 Vpp total)
MODE 4  FS  0..8 V full-scale, dummy-load only
```

Separate amplitude selector for P+/P-:

```text
GAIN 1.00
GAIN 1.50
GAIN 2.00
GAIN 2.15
GAIN 3.00
```

The exact set may be reduced after real measurement.

---

## 4. Controlled architecture

Do not build five unrelated analog circuits.

Use a common normalized source and common protected output stage:

```text
VIDEO_NORM
    |
amplitude block
    |
polarity block
    |
anchor/centering block
    |
output buffer
    |
protection
    |
TP_VIDEO_OUT
```

Control variables:

```text
AMPLITUDE  -> slope magnitude
POLARITY   -> sign
ANCHOR     -> black-at-V0 / centered-at-V0 / ground-referenced full-scale
```

This makes the hypotheses reproducible and independently testable.

---

## 5. Mathematical mode table

Let `x` be normalized luminance 0..1.

| Mode | Equation | Black | 50% | White |
|---|---|---:|---:|---:|
| P+ | `V0 + A*x` | V0 | V0+A/2 | V0+A |
| P- | `V0 - A*x` | V0 | V0-A/2 | V0-A |
| P± | `V0 + AP*(2x-1)` | V0-AP | V0 | V0+AP |
| FS+ | `VFS*x` | 0 | VFS/2 | VFS |
| FS- | `VFS*(1-x)` | VFS | VFS/2 | 0 |

The table is a test model, not a claim about the original Seiko circuit.

---

## 6. Measurement that distinguishes the families

Use the original TR02-01 with A00/A01/A02.

Record DC-coupled values:

```text
VB = pin-6 voltage on BLACK
VG = pin-6 voltage on 50% GRAY
VW = pin-6 voltage on WHITE
```

Then classify:

### P+

```text
VB < VG < VW
and VB approximately the reported DC reference
```

### P-

```text
VB > VG > VW
and VB approximately the reported DC reference
```

### P±

```text
VG approximately V0
VB and VW approximately symmetric around VG
```

### FS

```text
one endpoint approaches ground and the other approaches the large reported voltage
```

A03 grayscale steps provide a stronger linearity check than only three points.

---

## 7. Oscilloscope rule

For classification, the decisive capture must be **DC coupled**.

AC coupling is useful only for comparing excursion magnitude.

AC coupling removes the very information needed to distinguish:

- black-anchored P+;
- black-anchored P-;
- centered P±;
- full-scale FS.

Always save both:

```text
DC-coupled capture
AC-coupled excursion capture
```

with the same pattern and scope scale documented.

---

## 8. Safety hierarchy

Until original measurements exist:

```text
lowest-risk bench hypothesis:
P+ or P- with small excursion around a controlled V0

intermediate:
P± with bounded excursion

highest-risk:
FS 0..8 V / 8..0 V
```

This is a bench-risk ordering only, not a probability ranking.

No mode is connected to the wrist merely because it can be generated.

---

## 9. Probability note

Current qualitative expectation:

- P+ or P- around a DC operating point are the leading hypotheses;
- P± centered around the operating point is less likely but plausible enough to test;
- FS 0..8 V is a separate high-swing hypothesis and requires especially strong evidence.

These are engineering priors, not conclusions.

---

## 10. Required update to the dual-path bench

The existing `video-conditioning-dual-path-test-v0.1.md` covers only:

```text
positive-going, black-anchored:
UNITY+BIAS vs GAIN+BIAS
```

It remains valid for that subproblem.

This document expands the overall experiment to include:

- negative polarity;
- centered bipolar waveform;
- large full-scale waveform.

The dual-path bench must therefore be treated as **Phase 1** of the wider pin-6 waveform characterization.
